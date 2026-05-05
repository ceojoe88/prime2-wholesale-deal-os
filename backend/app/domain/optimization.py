from __future__ import annotations

from collections import Counter, defaultdict

from sqlalchemy.orm import Session

from app.models import (
    AgentPerformanceScore,
    OptimizationRecommendation,
    OutcomeLearningRecord,
    ScoringWeightChange,
)
from app.serializers import model_to_dict


UNSUPPORTED_OPTIMIZATION_PATTERNS = {
    "guaranteed_revenue": ["guaranteed revenue", "guaranteed assignment fee", "guaranteed profit"],
    "unsupported_roi": ["guaranteed roi", "risk-free return", "double your money"],
    "fake_numbers": ["invented arv", "fake repairs", "made-up spread"],
}


def validate_learning_record(record: OutcomeLearningRecord) -> dict[str, object]:
    reasons: list[str] = []
    if not record.source_records_present or not record.source_evidence_ids:
        reasons.append("source_evidence_required")
    if record.unsupported_revenue_claim:
        reasons.append("unsupported_revenue_claim")
    if record.unsupported_roi_claim:
        reasons.append("unsupported_roi_claim")
    if record.projected_assignment_fee and not record.source_records_present:
        reasons.append("projected_fee_needs_source_records")

    record.evidence_status = "supported" if not reasons else "blocked"
    return {
        "allowed": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "source_records_required": True,
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }


def validate_optimization_claim(content: str) -> dict[str, object]:
    text = content.lower()
    risk_flags = sorted(
        {
            category
            for category, phrases in UNSUPPORTED_OPTIMIZATION_PATTERNS.items()
            if any(phrase in text for phrase in phrases)
        }
    )
    return {
        "allowed": not risk_flags,
        "risk_flags": risk_flags,
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }


def agent_performance_overall(score: AgentPerformanceScore) -> float:
    overall = (
        score.quality_score * 0.18
        + score.conversion_score * 0.18
        + score.accuracy_score * 0.18
        + score.effectiveness_score * 0.16
        + (100 - score.compliance_block_rate) * 0.10
        + score.follow_up_score * 0.10
        + score.recommendation_accuracy * 0.10
    )
    score.overall_score = round(overall, 2)
    return score.overall_score


def _top_counter(records: list[OutcomeLearningRecord], attr: str) -> list[dict[str, object]]:
    grouped: dict[str, list[OutcomeLearningRecord]] = defaultdict(list)
    for record in records:
        grouped[getattr(record, attr)].append(record)
    items = []
    for key, rows in grouped.items():
        successful = [
            row
            for row in rows
            if row.conversion_result in {"contract_ready", "closed_verified", "assigned"}
        ]
        projected = sum(row.projected_assignment_fee for row in rows)
        verified = sum(row.verified_assignment_fee for row in rows)
        items.append(
            {
                attr: key,
                "record_count": len(rows),
                "success_count": len(successful),
                "success_rate": round((len(successful) / len(rows)) * 100, 2) if rows else 0,
                "projected_assignment_fee": projected,
                "verified_assignment_fee": verified,
                "explainable_basis": [row.id for row in rows],
            }
        )
    return sorted(
        items,
        key=lambda item: (item["success_rate"], item["verified_assignment_fee"], item["projected_assignment_fee"]),
        reverse=True,
    )


def detect_patterns(records: list[OutcomeLearningRecord]) -> dict[str, object]:
    blocker_counts = Counter(blocker for record in records for blocker in record.blockers)
    lost_counts = Counter(record.lost_reason for record in records if record.lost_reason)
    strong_10k = [
        model_to_dict(record)
        for record in records
        if record.projected_assignment_fee >= 10000
        and record.source_records_present
        and record.confidence_score >= 75
    ]
    return {
        "best_lead_types": _top_counter(records, "lead_source"),
        "best_zip_codes": _top_counter(records, "market"),
        "best_buyer_profiles": _top_counter(records, "buyer_type"),
        "best_offer_strategies": _top_counter(records, "offer_strategy"),
        "weak_seller_scripts": [
            {"follow_up_type": follow_up, "lost_count": count}
            for follow_up, count in Counter(
                record.follow_up_type
                for record in records
                if record.conversion_result in {"lost", "stalled"}
            ).most_common()
        ],
        "stale_follow_up_patterns": [
            model_to_dict(record)
            for record in records
            if "stale_follow_up" in record.blockers
        ],
        "buyer_pof_bottlenecks": blocker_counts.get("buyer_pof_gap", 0),
        "deals_dying_before_contract_ready": [
            model_to_dict(record)
            for record in records
            if record.conversion_result in {"lost", "stalled", "blocked"}
        ],
        "strong_10k_probability": strong_10k,
        "top_blockers": [
            {"blocker": blocker, "count": count}
            for blocker, count in blocker_counts.most_common()
        ],
        "lost_reasons": [
            {"lost_reason": reason, "count": count}
            for reason, count in lost_counts.most_common()
        ],
        "deterministic": True,
        "black_box_ml": False,
    }


def recommendation_summary(recommendation: OptimizationRecommendation) -> dict[str, object]:
    return {
        **model_to_dict(recommendation),
        "explainable": bool(recommendation.explanation and recommendation.source_record_ids),
        "guaranteed_revenue_claim_allowed": False,
        "unsupported_roi_claim_allowed": False,
    }


def optimization_dashboard(session: Session) -> dict[str, object]:
    records = session.query(OutcomeLearningRecord).all()
    recommendations = session.query(OptimizationRecommendation).all()
    agent_scores = session.query(AgentPerformanceScore).all()
    changes = session.query(ScoringWeightChange).all()
    for record in records:
        validate_learning_record(record)
    for score in agent_scores:
        agent_performance_overall(score)
    return {
        "outcome_learning_records": [model_to_dict(record) for record in records],
        "patterns": detect_patterns(records),
        "optimization_recommendations": [
            recommendation_summary(recommendation)
            for recommendation in sorted(
                recommendations,
                key=lambda item: (item.impact_score, item.confidence_score),
                reverse=True,
            )
        ],
        "agent_performance_scores": [
            model_to_dict(score)
            for score in sorted(agent_scores, key=lambda item: item.overall_score, reverse=True)
        ],
        "scoring_weight_changes": [model_to_dict(change) for change in changes],
        "lost_deals": [
            model_to_dict(record)
            for record in records
            if record.conversion_result in {"lost", "stalled", "blocked"}
        ],
        "source_quality": _top_counter(records, "lead_source"),
        "feedback_loop": {
            "updates_opportunity_scoring_weights": True,
            "updates_buyer_ranking_weights": True,
            "updates_follow_up_priority": True,
            "updates_market_heat": True,
            "updates_source_quality": True,
            "changes_logged": len(changes),
            "deterministic_explainable_scoring": True,
        },
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }
