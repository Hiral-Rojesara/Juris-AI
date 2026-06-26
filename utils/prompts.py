def legal_analysis_prompt(text):

    return f"""
    Analyze this Indian legal document.

    Provide:

    1. Document Type
    2. Important Parties
    3. Important Dates
    4. Important Clauses
    5. Legal Meaning
    6. Risks
    7. Summary

    Document:
    {text}
    """