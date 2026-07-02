def match_ratio(matches: list[dict]) -> float:
    if not matches:
        return 1.0

    met = sum(1 for item in matches if item.get("status") == "met")
    return met / len(matches)


def priority_category_score(category_assessment: dict) -> float:
    total = sum(item["weighted_value"] for item in category_assessment.values())

    if total == 0:
        return 0

    earned = sum(
        item["weighted_value"]
        for item in category_assessment.values()
        if item["status"] == "met"
    )

    return earned / total


def evidence_quality_score(summary_by_category: dict) -> float:
    if not summary_by_category:
        return 0

    strong = 0

    for data in summary_by_category.values():
        if data.get("evidence") and data.get("confidence") in ["High", "Medium"]:
            strong += 1

    return strong / len(summary_by_category)


def calculate_score(required_matches, preferred_matches, category_assessment, summary_by_category):
    required = match_ratio(required_matches) * 45
    priority = priority_category_score(category_assessment) * 35
    preferred = match_ratio(preferred_matches) * 10
    evidence = evidence_quality_score(summary_by_category) * 10

    return round(required + priority + preferred + evidence)