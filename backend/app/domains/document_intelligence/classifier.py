from __future__ import annotations


DOCUMENT_TYPES = {
    "purchase_agreement",
    "assignment_agreement",
    "proof_of_funds",
    "title_doc",
    "seller_doc",
    "buyer_doc",
    "inspection_notes",
    "repair_estimate",
    "comp_report",
    "other",
}

KEYWORDS: list[tuple[str, list[str]]] = [
    ("purchase_agreement", ["purchase agreement", "purchase price", "seller:", "buyer:"]),
    ("assignment_agreement", ["assignment agreement", "assignor", "assignee", "assignment fee"]),
    ("proof_of_funds", ["proof of funds", "available funds", "bank letter", "pof"]),
    ("title_doc", ["title company", "commitment", "escrow", "closing agent"]),
    ("inspection_notes", ["inspection", "access notes", "condition notes"]),
    ("repair_estimate", ["repair estimate", "scope of work", "contractor estimate"]),
    ("comp_report", ["comparable sale", "comp report", "arv range"]),
    ("seller_doc", ["seller disclosure", "seller document"]),
    ("buyer_doc", ["buyer entity", "buyer document"]),
]


def classify_document(
    *,
    filename: str = "",
    text: str = "",
    manual_document_type: str | None = None,
) -> dict[str, object]:
    normalized_manual = (manual_document_type or "").strip().lower()
    if normalized_manual in DOCUMENT_TYPES:
        return {
            "document_type": normalized_manual,
            "confidence_score": 100.0,
            "classification_reasons": ["manual_document_type"],
        }

    haystack = f"{filename} {text}".lower()
    scores: dict[str, int] = {}
    for document_type, terms in KEYWORDS:
        scores[document_type] = sum(1 for term in terms if term in haystack)
    document_type, score = max(scores.items(), key=lambda item: item[1])
    if score == 0:
        return {
            "document_type": "other",
            "confidence_score": 35.0,
            "classification_reasons": ["no_strong_keyword_match"],
        }
    return {
        "document_type": document_type,
        "confidence_score": min(95.0, 45.0 + score * 15.0),
        "classification_reasons": [f"matched_{score}_keywords"],
    }

