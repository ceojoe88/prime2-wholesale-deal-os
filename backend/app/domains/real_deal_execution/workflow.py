from __future__ import annotations


ALLOWED_BATCH_STATUSES = {
    "draft",
    "active",
    "calling",
    "underwriting",
    "offer_decision",
    "buyer_validation",
    "contract_ready",
    "completed",
    "archived",
}

CALL_CHECKLIST = [
    "verify_owner_identity",
    "verify_property_address",
    "confirm_occupancy",
    "ask_motivation_reason",
    "ask_timeline",
    "ask_property_condition",
    "ask_asking_price",
    "ask_decision_maker_status",
    "ask_mortgage_title_issue",
    "set_next_step",
    "log_dnc_if_requested",
]


def validate_batch_status(status: str) -> str:
    if status not in ALLOWED_BATCH_STATUSES:
        raise ValueError(f"Unsupported execution batch status: {status}")
    return status


def call_checklist() -> list[dict[str, object]]:
    return [
        {
            "id": item,
            "label": item.replace("_", " ").title(),
            "required": True,
            "operator_capture_only": True,
        }
        for item in CALL_CHECKLIST
    ]

