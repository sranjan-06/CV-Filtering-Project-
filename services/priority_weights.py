from config import CATEGORY_WEIGHTS_BY_RANK


def convert_priority_order_to_weights(priority_order):
    return {
        category: CATEGORY_WEIGHTS_BY_RANK[index]
        for index, category in enumerate(priority_order)
    }