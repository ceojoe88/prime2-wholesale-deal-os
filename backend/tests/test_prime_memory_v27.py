from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.prime_memory.learning import (
    playbook_from_evidence,
    scoring_recommendation_gate,
    sync_learning_signal,
    validate_memory_item,
)
from app.domains.prime_memory.sanitizer import sanitize_memory_record
from app.domains.prime_memory.service import approved_memory_context
from app.main import app
from app.models import (
    LearningSignal,
    PlaybookRecommendation,
    PrimeMemoryItem,
    ScoringWeightRecommendation,
)


def test_memory_requires_source_evidence_and_blocks_unsupported_claims():
    memory = PrimeMemoryItem(
        memory_id="memory-test",
        memory_type="high_spread_market",
        source_domain="market_enrichment",
        source_record_id="market-test",
        summary="This market has guaranteed profit.",
        evidence_basis=[],
        status="approved",
    )
    gate = validate_memory_item(memory)
    assert gate["allowed"] is False
    assert "source_evidence_required" in gate["blocked_reasons"]
    assert "guaranteed profit" in gate["blocked_reasons"]
    assert memory.status == "needs_review"
    assert memory.portal_exposure_allowed is False


def test_learning_signal_compares_predicted_and_actual_without_auto_apply():
    signal = LearningSignal(
        signal_id="signal-test",
        signal_type="motivation",
        source_domain="field_testing",
        source_record_id="feedback-test",
        predicted_value="high motivation",
        actual_value="not interested",
        evidence_basis=["feedback-test"],
    )
    sync = sync_learning_signal(signal)
    assert sync["variance"] > 0
    assert sync["auto_applied"] is False
    assert signal.auto_applied is False
    assert "Prediction differed" in signal.explanation


def test_scoring_recommendation_is_explainable_and_not_auto_applied():
    recommendation = ScoringWeightRecommendation(
        recommendation_id="weight-test",
        scoring_area="lead_source_quality",
        current_weight=0.1,
        suggested_weight=0.12,
        reason="Field outcomes support a small adjustment.",
        evidence_count=2,
        source_signal_ids=["signal-test"],
        auto_apply_allowed=True,
    )
    gate = scoring_recommendation_gate(recommendation)
    assert gate["can_queue_for_owner_review"] is False
    assert "auto_apply_blocked" in gate["blocked_reasons"]
    assert recommendation.explainable is True
    assert recommendation.auto_apply_allowed is False


def test_playbook_recommendation_created_from_evidence_and_stays_draft_only():
    playbook = PlaybookRecommendation(
        playbook_id="playbook-test",
        playbook_type="seller_offer_explanation",
        target_context="repair-backed seller",
        recommendation="Use empathy and source-backed repair notes.",
        evidence_basis=["memory-001"],
        status="approved",
    )
    gate = playbook_from_evidence(playbook)
    assert gate["can_use_for_drafts"] is True
    assert gate["draft_only"] is True
    assert playbook.portal_exposure_allowed is False


def test_memory_sanitizer_hides_internal_strategy_externally():
    memory = PrimeMemoryItem(
        memory_id="memory-sanitize",
        memory_type="winning_seller_script",
        source_domain="call_intelligence",
        source_record_id="call-intel-001",
        summary="Safe summary",
        evidence_basis=["call-intel-001"],
        internal_strategy="Internal negotiation strategy.",
    )
    external = sanitize_memory_record(memory, external=True)
    assert "internal_strategy" not in external
    assert "source_record_id" not in external
    assert external["portal_exposure_allowed"] is False


def test_ai_context_uses_only_approved_memory():
    with TestClient(app) as client:
        dashboard = client.get("/api/v1/prime-memory")
    assert dashboard.status_code == 200
    context = dashboard.json()["approved_ai_context"]
    assert context
    assert all(item["context_only"] is True for item in context)
    assert all(item["unsupported_claims_allowed"] is False for item in context)


def test_prime_memory_routes_render_and_preserve_boundaries():
    with TestClient(app) as client:
        dashboard = client.get("/api/v1/prime-memory")
        patterns = client.get("/api/v1/prime-memory/patterns")
        signals = client.get("/api/v1/prime-memory/learning-signals")
        weights = client.get("/api/v1/prime-memory/scoring-weight-recommendations")
        playbooks = client.get("/api/v1/prime-memory/playbook-recommendations")
        detail = client.get("/api/v1/prime-memory/memory-001")

    assert dashboard.status_code == 200
    assert patterns.status_code == 200
    assert signals.status_code == 200
    assert weights.status_code == 200
    assert playbooks.status_code == 200
    assert detail.status_code == 200
    body = dashboard.json()
    assert body["deterministic_explainable_learning"] is True
    assert body["scoring_changes_auto_apply_allowed"] is False
    assert body["compliance_override_allowed"] is False
    assert body["portal_strategy_exposure_allowed"] is False
    assert weights.json()["auto_apply_allowed"] is False
