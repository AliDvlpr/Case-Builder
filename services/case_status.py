def calculate_case_status(case_json: dict) -> str:
    statuses = [
        field.get("status", "missing")
        for field in case_json.values()
        if isinstance(field, dict)
    ]

    if statuses and all(status == "complete" for status in statuses):
        return "complete"

    return "needs_review"