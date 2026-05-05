from __future__ import annotations

from app.models import (
    CallFollowUpRecommendation,
    CallIntelligenceSession,
    CallObjectionRecord,
    CallTranscriptInput,
    SellerSignalExtraction,
)
from app.serializers import model_to_dict


def sanitize_call_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def sanitize_session(session: CallIntelligenceSession) -> dict[str, object]:
    data = model_to_dict(session)
    data["live_response_generated"] = False
    return data


def sanitize_input(record: CallTranscriptInput) -> dict[str, object]:
    data = model_to_dict(record)
    data["raw_audio_processed"] = False
    data["live_call_recording"] = False
    return data


def sanitize_signal(record: SellerSignalExtraction) -> dict[str, object]:
    return model_to_dict(record)


def sanitize_objection(record: CallObjectionRecord) -> dict[str, object]:
    data = model_to_dict(record)
    data["draft_only"] = True
    data["live_response_allowed"] = False
    return data


def sanitize_follow_up(record: CallFollowUpRecommendation) -> dict[str, object]:
    data = model_to_dict(record)
    data["live_send_allowed"] = False
    return data

