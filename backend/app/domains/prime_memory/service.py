from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.prime_memory.learning import (
    memory_confidence_rollup,
    playbook_from_evidence,
    scoring_recommendation_gate,
    sync_learning_signal,
    validate_memory_item,
)
from app.domains.prime_memory.sanitizer import sanitize_memory_record
from app.models import (
    LearningSignal,
    PlaybookRecommendation,
    PrimeMemoryItem,
    ScoringWeightRecommendation,
)


APPROVED_AI_MEMORY_TYPES = {
    "winning_seller_script",
    "common_objection",
    "strong_buyer_profile",
    "high_spread_market",
    "campaign_performance_pattern",
}


def sync_prime_memory(session: Session) -> None:
    for memory in session.query(PrimeMemoryItem).all():
        validate_memory_item(memory)
    for signal in session.query(LearningSignal).all():
        sync_learning_signal(signal)
    for recommendation in session.query(ScoringWeightRecommendation).all():
        scoring_recommendation_gate(recommendation)
    for playbook in session.query(PlaybookRecommendation).all():
        playbook_from_evidence(playbook)
    session.flush()


def approved_memory_context(session: Session) -> list[dict[str, object]]:
    sync_prime_memory(session)
    memories = (
        session.query(PrimeMemoryItem)
        .filter(PrimeMemoryItem.status == "approved", PrimeMemoryItem.owner_approved.is_(True))
        .all()
    )
    allowed = [
        memory
        for memory in memories
        if memory.memory_type in APPROVED_AI_MEMORY_TYPES and validate_memory_item(memory)["allowed"]
    ]
    return [
        {
            "memory_id": memory.memory_id,
            "memory_type": memory.memory_type,
            "summary": memory.summary,
            "evidence_basis": memory.evidence_basis,
            "confidence_score": memory.confidence_score,
            "context_only": True,
            "unsupported_claims_allowed": False,
        }
        for memory in allowed
    ]


def prime_memory_dashboard(session: Session) -> dict[str, object]:
    sync_prime_memory(session)
    memories = session.query(PrimeMemoryItem).all()
    signals = session.query(LearningSignal).all()
    scoring = session.query(ScoringWeightRecommendation).all()
    playbooks = session.query(PlaybookRecommendation).all()
    approved_memories = [
        memory for memory in memories if memory.status == "approved" and memory.owner_approved
    ]
    return {
        "memory_items": [sanitize_memory_record(memory) for memory in memories],
        "learning_signals": [
            {**sanitize_memory_record(signal), "sync": sync_learning_signal(signal)}
            for signal in signals
        ],
        "scoring_weight_recommendations": [
            {**sanitize_memory_record(item), "gate": scoring_recommendation_gate(item)}
            for item in scoring
        ],
        "playbook_recommendations": [
            {**sanitize_memory_record(item), "gate": playbook_from_evidence(item)}
            for item in playbooks
        ],
        "approved_ai_context": approved_memory_context(session),
        "top_learning_insights": [
            sanitize_memory_record(memory)
            for memory in sorted(approved_memories, key=lambda item: item.confidence_score, reverse=True)[:5]
        ],
        "pattern_summary": {
            "winning_scripts": len([m for m in memories if m.memory_type == "winning_seller_script"]),
            "weak_sources": len([m for m in memories if m.memory_type == "low_quality_lead_source"]),
            "high_spread_markets": len([m for m in memories if m.memory_type == "high_spread_market"]),
            "document_issue_patterns": len([m for m in memories if m.memory_type == "document_issue_pattern"]),
            "campaign_patterns": len([m for m in memories if m.memory_type == "campaign_performance_pattern"]),
            "confidence_rollup": memory_confidence_rollup(approved_memories),
        },
        "integration_signals": {
            "operator_mode_top_learning_insights": True,
            "ai_gateway_context_only": True,
            "campaign_brain_uses_approved_playbooks": True,
            "market_enrichment_flags_strong_weak_markets": True,
            "lead_qa_source_quality_warnings": True,
            "underwriting_similar_deal_warning": True,
            "buyer_disposition_repeat_reliable_buyers": True,
        },
        "deterministic_explainable_learning": True,
        "scoring_changes_auto_apply_allowed": False,
        "compliance_override_allowed": False,
        "portal_strategy_exposure_allowed": False,
    }


def memory_detail(session: Session, memory_id: str) -> dict[str, object]:
    memory = session.get(PrimeMemoryItem, memory_id)
    if memory is None:
        raise ValueError(f"Memory not found: {memory_id}")
    return {
        "memory": sanitize_memory_record(memory),
        "external_safe_memory": sanitize_memory_record(memory, external=True),
        "gate": validate_memory_item(memory),
        "context_only": True,
        "cannot_override_compliance": True,
    }

