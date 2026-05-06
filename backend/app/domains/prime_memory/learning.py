from __future__ import annotations

from app.domain.scoring import clamp_score
from app.models import (
    LearningSignal,
    PlaybookRecommendation,
    PrimeMemoryItem,
    ScoringWeightRecommendation,
)


UNSUPPORTED_MEMORY_PATTERNS = {
    "guaranteed profit",
    "guaranteed roi",
    "guaranteed close",
    "risk-free",
    "always converts",
    "legal conclusion",
}


def scan_memory_claims(text: str) -> dict[str, object]:
    lowered = text.lower()
    flags = sorted(pattern for pattern in UNSUPPORTED_MEMORY_PATTERNS if pattern in lowered)
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "unsupported_claims_blocked": bool(flags),
        "guaranteed_claims_allowed": False,
    }


def validate_memory_item(memory: PrimeMemoryItem) -> dict[str, object]:
    blocked_reasons: list[str] = []
    if not memory.evidence_basis:
        blocked_reasons.append("source_evidence_required")
    if not memory.source_record_id:
        blocked_reasons.append("source_record_required")
    safety = scan_memory_claims(" ".join([memory.summary or "", memory.internal_strategy or ""]))
    blocked_reasons.extend(str(flag) for flag in safety["risk_flags"])
    memory.unsupported_claims_blocked = True
    memory.portal_exposure_allowed = False
    if blocked_reasons and memory.status == "approved":
        memory.status = "needs_review"
    return {
        "allowed": not blocked_reasons,
        "blocked_reasons": sorted(set(blocked_reasons)),
        "unsupported_claims_blocked": True,
        "portal_exposure_allowed": False,
    }


def sync_learning_signal(signal: LearningSignal) -> dict[str, object]:
    predicted = str(signal.predicted_value or "").strip().lower()
    actual = str(signal.actual_value or "").strip().lower()
    if not signal.evidence_basis:
        signal.confidence = min(signal.confidence or 0, 35)
        signal.variance = max(signal.variance or 0, 60)
        signal.explanation = signal.explanation or "Evidence basis is missing, so learning confidence is capped."
    elif predicted == actual:
        signal.variance = 0
        signal.confidence = max(signal.confidence or 0, 90)
        signal.explanation = signal.explanation or "Prediction matched the observed outcome."
    else:
        signal.variance = signal.variance or 50
        signal.confidence = signal.confidence or 65
        signal.explanation = signal.explanation or "Prediction differed from the observed outcome and needs owner review."
    signal.auto_applied = False
    signal.unsupported_claims_blocked = True
    return {
        "variance": signal.variance,
        "confidence": signal.confidence,
        "explanation": signal.explanation,
        "auto_applied": False,
        "owner_review_required": signal.owner_review_status != "approved",
    }


def scoring_recommendation_gate(recommendation: ScoringWeightRecommendation) -> dict[str, object]:
    blocked_reasons: list[str] = []
    if recommendation.evidence_count <= 0 or not recommendation.source_signal_ids:
        blocked_reasons.append("evidence_required")
    if not recommendation.reason:
        blocked_reasons.append("reason_required")
    if recommendation.auto_apply_allowed:
        blocked_reasons.append("auto_apply_blocked")
    recommendation.explainable = True
    recommendation.auto_apply_allowed = False
    return {
        "can_queue_for_owner_review": not blocked_reasons,
        "blocked_reasons": sorted(set(blocked_reasons)),
        "auto_apply_allowed": False,
        "owner_approval_required": recommendation.owner_approval_status != "approved",
    }


def playbook_from_evidence(playbook: PlaybookRecommendation) -> dict[str, object]:
    blocked_reasons: list[str] = []
    if not playbook.evidence_basis:
        blocked_reasons.append("evidence_basis_required")
    safety = scan_memory_claims(playbook.recommendation or "")
    blocked_reasons.extend(str(flag) for flag in safety["risk_flags"])
    playbook.draft_only = True
    playbook.owner_review_required = True
    playbook.portal_exposure_allowed = False
    playbook.unsupported_claims_blocked = True
    if blocked_reasons and playbook.status == "approved":
        playbook.status = "needs_review"
    return {
        "can_use_for_drafts": not blocked_reasons and playbook.status == "approved",
        "blocked_reasons": sorted(set(blocked_reasons)),
        "draft_only": True,
        "owner_review_required": True,
    }


def memory_confidence_rollup(memories: list[PrimeMemoryItem]) -> float:
    if not memories:
        return 0
    return clamp_score(sum(memory.confidence_score for memory in memories) / len(memories))

