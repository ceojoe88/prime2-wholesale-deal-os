from __future__ import annotations


REQUIRED_CONFIRMATIONS = [
    "contract reviewed by attorney/title company",
    "seller understands role",
    "buyer understands assignment",
    "assignment fee disclosure reviewed",
    "no legal advice provided",
    "no misrepresentation",
]


def compliance_checklists(state: str = "local") -> dict[str, object]:
    return {
        "purchase_agreement_checklist": [
            "Confirm owner approval before preparing an offer packet",
            "Verify seller identity and authority to sign",
            "Document ARV and repair assumptions",
            "Confirm inspection and title review timelines",
            "Route agreement to attorney/title company before execution",
        ],
        "assignment_agreement_checklist": [
            "Confirm seller contract is valid and assignable",
            "Confirm buyer proof of funds and closing timeline",
            "Review assignment fee disclosure",
            "Route assignment packet to attorney/title company",
            "Block execution until owner approval is recorded",
        ],
        "title_company_checklist": [
            "Open file only after owner approval",
            "Provide purchase agreement for review",
            "Confirm assignment workflow is acceptable in the jurisdiction",
            "Track title defects, payoff, liens, and closing blockers",
        ],
        "seller_disclosure_checklist": [
            "Disclose role accurately",
            "Avoid pressure or guaranteed outcomes",
            "Keep offer basis tied to documented assumptions",
        ],
        "buyer_disclosure_checklist": [
            "Disclose assignment nature",
            "Do not represent unverified facts",
            "Confirm buyer diligence responsibility",
        ],
        "state_compliance_risk_warning": (
            f"State-specific compliance for {state} must be reviewed by qualified counsel "
            "or a title professional before contracts or assignments are executed."
        ),
        "attorney_title_review_reminder": True,
        "required_confirmations": REQUIRED_CONFIRMATIONS,
    }
