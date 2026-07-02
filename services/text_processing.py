def clean_text(text):
    return " ".join(text.split())


def is_empty_or_whitespace(text):
    return not text or not text.strip()