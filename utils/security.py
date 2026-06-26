# =========================================================
# SECURITY FUNCTIONS
# =========================================================

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_TYPES = [
    "image/png",
    "image/jpeg"
]

BLOCKED_WORDS = [
    "ignore previous instructions",
    "system prompt",
    "hack",
    "bypass",
    "jailbreak"
]


def validate_file(uploaded_file):

    if uploaded_file.size > MAX_FILE_SIZE:

        return False, "⚠️ File too large. Max 5MB allowed."

    if uploaded_file.type not in ALLOWED_TYPES:

        return False, "⚠️ Only PNG and JPG allowed."

    return True, "Valid File"


def check_prompt_safety(prompt):

    for word in BLOCKED_WORDS:

        if word.lower() in prompt.lower():

            return False

    return True