from groq import Groq
import streamlit as st

from utils.security import check_prompt_safety

# =========================================================
# GROQ CLIENT
# =========================================================

api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

# =========================================================
# AI FUNCTION
# =========================================================

def ask_juris_ai(prompt, lang="English"):

    safe = check_prompt_safety(prompt)

    if not safe:

        return "⚠️ Unsafe query detected."

    full_prompt = f"""
    You are Juris-AI.

    Respond in {lang}.

    User Query:
    {prompt}
    """

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],

            temperature=0.3,
            max_tokens=2048
        )

        return completion.choices[0].message.content

    except Exception:

        return "⚠️ AI system error."