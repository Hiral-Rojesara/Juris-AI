import re
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from utils.pdf_loader import load_pdf_text
from utils.section_search import search_section
# =========================================================
# LAW DATABASE
# =========================================================

@st.cache_data
def load_law_database():

    return {

        "BNS": load_pdf_text("data/BNS/BNS.pdf"),

        "BNSS": load_pdf_text("data/BNSS/BNSS.pdf"),

        "BSA": load_pdf_text("data/BSA/BSA.pdf"),

        "IPC": load_pdf_text("data/IPC/IPC.pdf"),

        "CRPC": load_pdf_text("data/CRPC/CrPC.pdf"),

        "CPC": load_pdf_text("data/CPC/CPC.pdf"),

        "EVIDENCE": load_pdf_text(
            "data/EVIDENCE/Evidence1872.pdf"
        ),

        "CONSTITUTION": load_pdf_text(
            "data/CONSTITUTION/Constitution.pdf"
        )
    }

# LAW_DATABASE = load_law_database()

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Juris-AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# =========================================================
# SESSION STATE
# =========================================================

if "scanner_result" not in st.session_state:
    st.session_state["scanner_result"] = ""

if "legal_response" not in st.session_state:
    st.session_state["legal_response"] = ""

if "law_result" not in st.session_state:
    st.session_state["law_result"] = ""

if "draft_result" not in st.session_state:
    st.session_state["draft_result"] = ""

if "news_result" not in st.session_state:
    st.session_state["news_result"] = ""

# =========================================================
# GROQ CONFIG
# =========================================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(api_key=api_key)

    SYSTEM_READY = True

except Exception:

    SYSTEM_READY = False

# =========================================================
# LANGUAGE MAPS
# =========================================================

LANGUAGE_CODES = {

    "English": "en-IN",
    "Hindi (हिन्दी)": "hi-IN",
    "Gujarati (ગુજરાતી)": "gu-IN",
    "Marathi (मराठी)": "mr-IN",
    "Tamil (தமிழ்)": "ta-IN",
    "Telugu (తెలుగు)": "te-IN",
    "Kannada (ಕನ್ನಡ)": "kn-IN",
    "Malayalam (മലയാളം)": "ml-IN",
    "Punjabi (ਪੰਜਾਬੀ)": "pa-IN",
    "Bengali (বাংলা)": "bn-IN",
    "Urdu (اردو)": "ur-IN"
}

OCR_LANGS = {

    "English": "eng",
    "Hindi (हिन्दी)": "hin",
    "Gujarati (ગુજરાતી)": "guj",
    "Marathi (मराठी)": "mar",
    "Tamil (தமிழ்)": "tam",
    "Telugu (తెలుగు)": "tel",
    "Kannada (ಕನ್ನಡ)": "kan",
    "Malayalam (മലയാളം)": "mal",
    "Punjabi (ਪੰਜਾਬੀ)": "pan",
    "Bengali (বাংলা)": "ben",
    "Urdu (اردو)": "urd"
}

# =========================================================
# FUNCTIONS
# =========================================================

def preprocess_image(image):

    image = image.convert("L")

    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(3)

    image = image.filter(ImageFilter.SHARPEN)

    image = image.filter(ImageFilter.MedianFilter())

    return image


def speak_text(text, lang_code="en-IN"):

    if not text:
        return

    clean_text = re.sub(r"[`]", "", text)

    clean_text = clean_text.replace("\n", " ")

    js_code = f"""
    <script>

    const synth = window.speechSynthesis;

    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(
        `{clean_text}`
    );

    utterance.lang = "{lang_code}";
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    synth.speak(utterance);

    </script>
    """

    components.html(js_code, height=0)


def ask_juris_ai(prompt, lang="English"):

    if not SYSTEM_READY:

        return """
        ⚠️ GROQ API ERROR

        Add your API key inside:

        .streamlit/secrets.toml
        """

    full_prompt = f"""
    You are Juris-AI.

    You are an expert Indian legal assistant.

    IMPORTANT:
    - Respond only in {lang}
    - Use simple language
    - Explain properly
    - Avoid difficult legal words
    - Structure response clearly
    - Mention users should consult lawyers for critical matters

    User Query:
    {prompt}
    """

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Indian legal AI assistant."
                    )
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],

            temperature=0.3,
            max_tokens=2048
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"⚠️ API Error: {str(e)}"



# =========================================================
# UI DESIGN
# =========================================================

st.markdown("""
<style>

.stApp{
    background:#ffffff;
}

[data-testid="stSidebar"]{
    display:none;
}

.main-title{
    background:linear-gradient(90deg,#1E3A8A,#2563EB);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.box{
    background:#F8FAFC;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #2563EB;
    margin-bottom:20px;
}

.footer{
    text-align:center;
    padding:15px;
    margin-top:30px;
    border-top:2px solid #2563EB;
    font-weight:bold;
}

</style>

<div class="main-title">
<h1>⚖️ JURIS-AI</h1>
<h4>Multilingual Indian Legal AI Platform</h4>
</div>

""", unsafe_allow_html=True)

# =========================================================
# LANGUAGE SELECTOR
# =========================================================

_, lang_col = st.columns([4,1])

user_lang = lang_col.selectbox(

    "🌍 Language",

    list(LANGUAGE_CODES.keys()),

    key="main_language"
)

voice_lang = LANGUAGE_CODES.get(user_lang, "en-IN")

ocr_lang = OCR_LANGS.get(user_lang, "eng")

# =========================================================
# TABS
# =========================================================

tabs = st.tabs([
    "📄 Smart Scanner",
    "🧠 AI Legal Advisor",
    "📚 Law Library",
    "✍️ Draft Generator",
    "🏛️ Court Finder",
    "📰 Legal Updates",
    "ℹ️ About"
])

# =========================================================
# TAB 1 — SMART SCANNER
# =========================================================

with tabs[0]:

    st.subheader("📄 AI Legal Document Scanner")

    st.info(
        "Upload clear legal document image for better OCR accuracy."
    )

    uploaded_file = st.file_uploader(

        "Upload Legal Document",

        type=["png", "jpg", "jpeg"],

        key="scanner_uploader"
    )

    if uploaded_file:

        MAX_FILE_SIZE = 5 * 1024 * 1024

        if uploaded_file.size > MAX_FILE_SIZE:

            st.error(
                "⚠️ File too large. Upload image below 5MB."
            )

            st.stop()

        try:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Document",
                use_container_width=True
            )

            processed_image = preprocess_image(image)

            if st.button(
                "🚀 Extract & Analyze",
                use_container_width=True,
                key="analyze_btn"
            ):

                with st.spinner("Scanning document..."):

                    try:

                        extracted_text = pytesseract.image_to_string(

                            processed_image,

                            lang=ocr_lang,

                            config="--psm 6"
                        )

                    except:

                        extracted_text = pytesseract.image_to_string(

                            processed_image,

                            lang="eng",

                            config="--psm 6"
                        )

                    extracted_text = " ".join(
                        extracted_text.split()
                    )

                if not extracted_text.strip():

                    st.error(
                        "⚠️ No readable text found."
                    )

                else:

                    st.success(
                        "✅ Text Extracted Successfully"
                    )

                    st.text_area(

                        "📄 Extracted Text",

                        extracted_text,

                        height=250,

                        key="ocr_text"
                    )

                    st.download_button(

                        "📥 Download Text",

                        extracted_text,

                        file_name="legal_text.txt",

                        key="download_ocr"
                    )

                    with st.spinner(
                        "Analyzing legal document..."
                    ):

                        prompt = f"""
                        You are an Indian legal AI expert.

                        Analyze this legal document carefully.

                        Respond ONLY in {user_lang}.

                        Use simple citizen-friendly language.

                        Provide:

                        1. Document Type
                        2. Main Parties
                        3. Important Dates
                        4. Important Clauses
                        5. Legal Meaning
                        6. Hidden Risks
                        7. Missing Information
                        8. Legal Sensitivity Level
                        9. Citizen Advice
                        10. Simple Summary

                        Also detect:
                        - Fraud risk
                        - Suspicious clauses
                        - Unsafe legal wording

                        Document:
                        {extracted_text}
                        """

                        result = ask_juris_ai(
                            prompt,
                            user_lang
                        )

                        st.session_state[
                            "scanner_result"
                        ] = result

            if st.session_state.get("scanner_result"):

                st.markdown("## ⚖️ AI Legal Analysis")

                st.write(
                    st.session_state["scanner_result"]
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(

                        "📥 Download Analysis",

                        st.session_state["scanner_result"],

                        file_name="legal_analysis.txt",

                        key="download_analysis"
                    )

                with col2:

                    if st.button(
                        "🔊 Read Analysis",
                        use_container_width=True,
                        key="read_analysis"
                    ):

                        speak_text(
                            st.session_state["scanner_result"],
                            voice_lang
                        )

        except Exception as e:

            st.error(f"⚠️ Scanner Error: {str(e)}")

# =========================================================
# TAB 2 — AI LEGAL ADVISOR
# =========================================================

with tabs[1]:

    st.subheader("🧠 Ask Legal Questions")

    legal_question = st.text_area(

        "Enter your legal question",

        key="legal_question"
    )

    if st.button(
        "⚖️ Get Legal Guidance",
        key="legal_query_btn"
    ):

        with st.spinner("Generating response..."):

            response = ask_juris_ai(
                legal_question,
                user_lang
            )

            st.session_state[
                "legal_response"
            ] = response

    if st.session_state.get("legal_response"):

        st.write(
            st.session_state["legal_response"]
        )

        if st.button(
            "🔊 Read Response",
            key="read_legal_response"
        ):

            speak_text(
                st.session_state["legal_response"],
                voice_lang
            )
## =========================================================
# TAB 3 — LAW LIBRARY
# =========================================================

with tabs[2]:

    st.subheader("📚 Indian Law Library")

    law_query = st.text_input(
        "Enter Example: BNS-103, IPC-302, CRPC-101, CPC-25"
    )
    LAW_DATABASE = load_law_database()
    if st.button("🔍 Search Law"):

        try:
            parts = law_query.upper().split()

            act = parts[0]
            section = parts[1]

            act_text = LAW_DATABASE.get(act)

            if not act_text:

                st.error("Act not found")

            else:

                section_text = search_section(
                    act_text,
                    section
                )

                if not section_text:

                    st.error(
                        "Section not found"
                    )

                else:

                    st.markdown(
                        "### 📜 Original Section"
                    )

                    st.text_area(
                        "Section Text",
                        section_text,
                        height=500,
                        key="section_text"
                    )

                    explain_prompt = f"""
                    Explain this legal section
                    in simple {user_lang} language.

                    Section:
                    {section_text}
                    """

                    explanation = ask_juris_ai(
                        explain_prompt,
                        user_lang
                    )

                    st.markdown(
                        "### ⚖️ Simplified Explanation"
                    )

                    st.write(explanation)

        except Exception:

            st.error(
                "Use format: BNS 103"
            )
# =========================================================
# TAB 4 — DRAFT GENERATOR
# =========================================================

with tabs[3]:

    st.subheader("✍️ Legal Draft Generator")

    draft_type = st.selectbox(

        "Select Draft Type",

        [
            "Affidavit",
            "Rent Agreement",
            "Legal Notice",
            "Sale Deed",
            "NDA"
        ],

        key="draft_select"
    )

    if st.button(
        "📄 Generate Draft",
        key="draft_btn"
    ):

        prompt = f"""
        Create professional Indian legal draft format for:

        {draft_type}

        Keep placeholders for names, dates and addresses.
        """

        result = ask_juris_ai(
            prompt,
            user_lang
        )

        st.text_area(
            "Generated Draft",
            result,
            height=350,
            key="draft_output"
        )

# =========================================================
# TAB 5 — COURT FINDER
# =========================================================

with tabs[4]:

    st.subheader("🏛️ Court Finder")

    city = st.text_input(
        "Enter City",
        key="court_city"
    )

    if st.button(
        "📍 Find Courts",
        key="court_btn"
    ):

        prompt = f"""
        List important courts in {city}, India.

        Include:
        - Court Name
        - Court Type
        - General Information
        """

        result = ask_juris_ai(
            prompt,
            user_lang
        )

        st.write(result)

# =========================================================
# TAB 6 — LEGAL NEWS
# =========================================================

with tabs[5]:

    st.subheader("📰 Indian Legal Updates")

    if st.button(
        "🔄 Load Legal Updates",
        key="news_btn"
    ):

        prompt = """
        Provide latest Indian legal developments,
        Supreme Court updates,
        constitutional discussions,
        and important reforms.
        """

        result = ask_juris_ai(
            prompt,
            user_lang
        )

        st.write(result)

# =========================================================
# TAB 7 — ABOUT
# =========================================================

with tabs[6]:

    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.header("👨‍💻 Founder & Lead Developer")

    st.subheader("Hiral Rojesara")

    st.write("AI Developer | Legal-Tech Innovator | Founder of Juris-AI")


    st.write("""
    Juris-AI is an AI-powered legal accessibility platform designed to bridge the gap between complex legal information and everyday citizens. 
    The platform leverages Artificial Intelligence, Optical Character Recognition (OCR), multilingual support, and voice technology to simplify legal understanding and improve access to legal information across India.

    The mission of Juris-AI is to make legal knowledge more accessible, understandable, and inclusive for individuals regardless of language, education, or geographical barriers.

    By combining advanced AI technologies with legal information systems, Juris-AI aims to empower citizens, students, researchers, and legal professionals with intelligent legal assistance and document analysis tools.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("🚀 Core Features")

    st.write("""
    ✅ AI-Powered Legal Assistance \n
    ✅ Multilingual Legal Information Access \n
    ✅ OCR-Based Legal Document Analysis\n
    ✅ Legal Risk & Clause Identification\n
    ✅ Voice-Assisted Legal Guidance\n
    ✅ Indian Law & Section Search Engine\n
    ✅ Legal Draft Generation Framework\n
    ✅ Citizen-Centric Legal Awareness Tools\n
    ✅ Court Information & Legal Resource Access\n
    ✅ AI-Enhanced Legal Research Support\n  
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("🛠️ Technology Stack")

    st.write("""
    • Frontend Framework: Streamlit\n
    • Programming Language: Python\n
    • Large Language Models (LLMs): Llama 3\n
    • AI Infrastructure: Groq API\n
    • Optical Character Recognition: Tesseract OCR\n
    • Prompt Engineering & Legal AI Workflows\n
    • Document Processing & Text Extraction\n
    • Multilingual Language Processing\n
    • AI-Based Legal Knowledge Retrieval\n
    • Speech Synthesis & Accessibility Features\n
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DISCLAIMER
# =========================================================

st.warning("""
⚠️ Juris-AI provides AI-generated legal information
for educational and accessibility purposes only.

This platform does not replace professional legal advice,
advocates, or certified legal consultation.
""")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    ⚖️ Juris-AI | AI-Powered Legal Accessibility Platform
    <br>
    Designed & Developed by Hiral Rojesara
    </div>
    """,
    unsafe_allow_html=True
)
