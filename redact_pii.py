import re

def redact_pii(text):
    patterns = [
        (r'\b[A-Z]{2,}-?\d{3,}\b', '[REDACTED_ID]'),
        (r'\b\d{10}\b', '[REDACTED_PHONE]'),
        (r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[REDACTED_EMAIL]'),
        (r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[REDACTED_DATE]'),
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    return text