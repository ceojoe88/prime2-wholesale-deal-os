from __future__ import annotations


UNSAFE_EXECUTION_TEXT = {
    "legal_guidance": ["legal advice", "legally binding", "no attorney needed"],
    "guaranteed_profit": ["guaranteed profit", "guarantee profit", "guaranteed fee"],
    "fake_urgency": ["last chance", "must sign today", "this will sell today"],
    "fake_buyer_claim": ["buyers lined up", "buyer is guaranteed"],
    "contract_execution": ["execute contract", "sign automatically"],
    "title_submission": ["submit to title automatically", "send to title now"],
}


def validate_execution_guidance_text(text: str) -> dict[str, object]:
    lowered = text.lower()
    flags = [
        category
        for category, patterns in UNSAFE_EXECUTION_TEXT.items()
        if any(pattern in lowered for pattern in patterns)
    ]
    return {
        "allowed": not flags,
        "risk_flags": sorted(set(flags)),
        "draft_only": True,
        "reason": "Guidance is safe for internal recommendation." if not flags else "Guidance requires owner/compliance review.",
    }


def execution_safety_boundary() -> dict[str, bool]:
    return {
        "live_outreach_allowed": False,
        "bulk_blast_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
        "legal_guidance_allowed": False,
        "guaranteed_profit_claim_allowed": False,
        "owner_final_approver": True,
    }

