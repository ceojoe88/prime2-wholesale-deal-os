from __future__ import annotations

import re


MONEY_RE = re.compile(r"\$?\s*([0-9]{2,3}(?:,[0-9]{3})+|[0-9]{5,7})")
DATE_RE = re.compile(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Z][a-z]+ \d{1,2}, \d{4})")


def _clean_price(value: str | None) -> int | None:
    if not value:
        return None
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else None


def _match_after(label: str, text: str) -> str:
    pattern = re.compile(rf"(?:{label})\s*[:\-]\s*([^\n\r;]+)", re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _price_after(labels: list[str], text: str) -> int | None:
    for label in labels:
        pattern = re.compile(rf"{label}\s*[:\-]?\s*\$?\s*([0-9,]{{5,12}})", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            return _clean_price(match.group(1))
    match = MONEY_RE.search(text)
    return _clean_price(match.group(1)) if match else None


def extract_document_fields(
    *,
    document_type: str,
    text: str,
    manual_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    manual_metadata = manual_metadata or {}
    seller = str(manual_metadata.get("seller_name") or _match_after("seller", text))
    buyer = str(manual_metadata.get("buyer_name") or _match_after("buyer|entity|assignee", text))
    property_address = str(
        manual_metadata.get("property_address")
        or _match_after("property address|address|subject property", text)
    )
    title_company = str(manual_metadata.get("title_company") or _match_after("title company", text))
    price = manual_metadata.get("purchase_price")
    if price is None:
        price = _price_after(["purchase price", "contract price", "offer amount", "price"], text)
    pof_amount = manual_metadata.get("pof_amount")
    if pof_amount is None:
        pof_amount = _price_after(["proof of funds", "available funds", "pof amount", "funds available"], text)

    dates = DATE_RE.findall(text)
    effective_date = str(manual_metadata.get("effective_date") or _match_after("effective date", text) or (dates[0] if dates else ""))
    closing_date = str(manual_metadata.get("closing_date") or _match_after("closing date", text) or (dates[1] if len(dates) > 1 else ""))
    lowered = text.lower()
    signature_status = str(manual_metadata.get("signature_status") or "")
    if not signature_status:
        if "unsigned" in lowered or "signature missing" in lowered:
            signature_status = "missing"
        elif "signed" in lowered or "seller signature" in lowered or "buyer signature" in lowered:
            signature_status = "signed"
        else:
            signature_status = "unknown"
    assignment_language_present = bool(
        manual_metadata.get("assignment_language_present")
        or "assignment allowed" in lowered
        or "may assign" in lowered
        or "right to assign" in lowered
        or "assignor" in lowered
        or "assignee" in lowered
    )

    repair_or_arv_claims = [
        phrase
        for phrase in ["arv", "after repair value", "repair estimate"]
        if phrase in lowered
    ]
    missing_fields: list[str] = []
    if document_type in {"purchase_agreement", "assignment_agreement", "seller_doc"} and not seller:
        missing_fields.append("seller_name")
    if document_type in {"purchase_agreement", "assignment_agreement", "buyer_doc", "proof_of_funds"} and not buyer:
        missing_fields.append("buyer_or_entity_name")
    if document_type in {"purchase_agreement", "assignment_agreement", "title_doc"} and not property_address:
        missing_fields.append("property_address")
    if document_type in {"purchase_agreement", "assignment_agreement"} and not price:
        missing_fields.append("purchase_price")
    if document_type in {"purchase_agreement", "assignment_agreement"} and not effective_date:
        missing_fields.append("effective_date")
    if document_type in {"purchase_agreement", "assignment_agreement", "title_doc"} and not closing_date:
        missing_fields.append("closing_date")
    if document_type in {"purchase_agreement", "assignment_agreement"} and signature_status != "signed":
        missing_fields.append("signature")
    if document_type == "assignment_agreement" and not assignment_language_present:
        missing_fields.append("assignment_language")
    if document_type == "proof_of_funds" and not pof_amount:
        missing_fields.append("pof_amount")

    return {
        "seller_name": seller,
        "buyer_name": buyer,
        "property_address": property_address,
        "effective_date": effective_date,
        "closing_date": closing_date,
        "signature_status": signature_status,
        "assignment_language_present": assignment_language_present,
        "pof_amount": int(pof_amount) if pof_amount else None,
        "purchase_price": int(price) if price else None,
        "title_company_name": title_company,
        "missing_fields": missing_fields,
        "repair_or_arv_claims": repair_or_arv_claims,
        "summary": _summary(document_type, property_address, price, pof_amount),
        "source_basis": {
            "manual_metadata_fields": sorted(manual_metadata.keys()),
            "text_length": len(text),
            "deterministic_fallback": True,
        },
    }


def _summary(document_type: str, address: str, price: object, pof_amount: object) -> str:
    if document_type == "proof_of_funds":
        return f"Proof-of-funds document with amount {pof_amount or 'missing'}."
    return f"{document_type.replace('_', ' ')} for {address or 'property not captured'} with price {price or 'missing'}."
