import re

def check_input(message):
    patterns = [
        r"ignore previous instructions",
        r"ignore all previous instructions",
        r"show me another member's claims",
        r"show me another member claims",
        r"give me another member's information",
        r"access another member"
    ]

    for pattern in patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False

    return True