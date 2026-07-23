import json

from .client import ai_client

ALLOWED_STATUSES = {"complete", "missing", "weak"}

SYSTEM_PROMPT = (
    "You are a senior Product Design mentor and UX hiring reviewer. "
    "You review a single field of a UX case study after the user edits it. "
    "You are given the full case study for context and the field that was just "
    "changed, with its new content. "
    "Decide the correct status for the changed field only: "
    '"complete" if it is filled in with enough detail to stand on its own, '
    '"weak" if it has content but is vague, thin, or underdeveloped, '
    '"missing" if it is empty, null, or effectively says nothing. '
    "Always return valid JSON only, in this exact shape: "
    '{"status": "complete" | "weak" | "missing", "reasoning": "one short sentence"}. '
    "Never use markdown. Never explain your output outside the JSON. "
    "Never invent information. If information is insufficient, assign the correct status."
)


class CaseEditorError(Exception):
    """Raised when the AI field-status evaluation cannot be completed."""


def _build_prompt(full_case: dict, field_name: str, field_content: str) -> str:
    return (
        "FULL CASE STUDY (for context):\n"
        f"{json.dumps(full_case, indent=2, ensure_ascii=False)}\n\n"
        f"FIELD CHANGED: {field_name}\n"
        f"NEW CONTENT:\n{field_content!r}\n\n"
        "Evaluate only this field and return the JSON object described in your instructions."
    )


def evaluate_field_status(full_case: dict, field_name: str, field_content: str) -> dict:
    """
    Ask the AI to evaluate a single updated field against the rest of the case
    and return {"status": ..., "reasoning": ...}.

    Raises CaseEditorError on any failure (bad request, network/API error,
    invalid JSON, invalid status) so the caller never has to handle a raw
    exception from the AI client.
    """
    if not field_name:
        raise CaseEditorError("No field name provided to evaluate.")

    prompt = _build_prompt(full_case, field_name, field_content or "")

    try:
        raw_content = ai_client.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
        )
    except Exception as exc:
        raise CaseEditorError(f"AI request failed: {exc}") from exc

    try:
        result = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise CaseEditorError("AI response was not valid JSON.") from exc

    status = result.get("status")
    if status not in ALLOWED_STATUSES:
        raise CaseEditorError(f"AI returned an invalid status: {status!r}")

    return {
        "status": status,
        "reasoning": result.get("reasoning", ""),
    }