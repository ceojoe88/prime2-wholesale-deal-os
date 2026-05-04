from __future__ import annotations

import csv
from io import StringIO


LEAD_SOURCE_CATEGORIES = {
    "absentee owner",
    "vacant",
    "tax delinquent",
    "probate",
    "inherited",
    "tired landlord",
    "code violation",
    "high equity",
    "pre-foreclosure",
    "driving for dollars",
    "county records",
}

REQUIRED_LEAD_COLUMNS = {
    "seller_name",
    "address",
    "city",
    "state",
    "zip_code",
    "source_category",
}


def preview_lead_csv(csv_text: str) -> dict[str, object]:
    reader = csv.DictReader(StringIO(csv_text))
    rows = list(reader)
    columns = set(reader.fieldnames or [])
    missing_columns = sorted(REQUIRED_LEAD_COLUMNS - columns)
    invalid_sources = sorted(
        {
            row.get("source_category", "").strip().lower()
            for row in rows
            if row.get("source_category", "").strip().lower()
            and row.get("source_category", "").strip().lower() not in LEAD_SOURCE_CATEGORIES
        }
    )
    return {
        "row_count": len(rows),
        "required_columns": sorted(REQUIRED_LEAD_COLUMNS),
        "missing_columns": missing_columns,
        "accepted_source_categories": sorted(LEAD_SOURCE_CATEGORIES),
        "invalid_sources": invalid_sources,
        "ready_for_import": not missing_columns and not invalid_sources,
        "draft_only": True,
    }
