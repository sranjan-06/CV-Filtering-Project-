from config import VALID_CATEGORIES, CATEGORY_WEIGHTS_BY_RANK


def convert_priority_order_to_weights(priority_order: list[str]) -> dict:
    if len(priority_order) != 5:
        raise ValueError("Employer must rank all five categories.")

    if set(priority_order) != set(VALID_CATEGORIES):
        raise ValueError("Priority order must contain exactly the five valid categories.")

    return {
        category: CATEGORY_WEIGHTS_BY_RANK[index]
        for index, category in enumerate(priority_order)
    }