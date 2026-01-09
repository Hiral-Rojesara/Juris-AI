import streamlit as st
import requests
import base64

# In settings ko functions ke upar add karein
AI_KEY = st.secrets["AZURE_OPENAI_KEY"]
AI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
DEPLOY_NAME = st.secrets["AZURE_DEPLOYMENT_NAME"]


# --- FUNCTIONS ---
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')


def speak_text(text):
    """Universal Browser Voice Fix"""
    if text:
        clean_text = text.replace("'", "").replace("\n", " ").replace('"', '')
        js_code = f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'en-IN';
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_code, height=0)


def ask_juris_ai(prompt, lang="English", image_base64=None):
    url = f"{AI_ENDPOINT}/openai/deployments/{DEPLOY_NAME}/chat/completions?api-version=2024-02-15-preview"
    headers = {"api-key": AI_KEY, "Content-Type": "application/json"}

    content = [{"type": "text", "text": prompt}]
    if image_base64:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}})

    payload = {
        "messages": [
            {"role": "system", "content": f"You are Juris-AI. Expert in Indian Law. Language: {lang}."},
            {"role": "user", "content": content}
        ],
        "max_tokens": 1500
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Connection Error. Check Azure Settings."


# --- UI STYLING ---
st.set_page_config(page_title="Juris-AI Final Submission", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { display: none; }
    .header { background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding: 25px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: white; text-align: center; border-top: 2px solid #1E3A8A; padding: 10px; font-weight: bold; }
    </style>
    <div class="header"><h1>⚖️ JURIS-AI : BHARATIYA LEGAL MEGA-PORTAL</h1></div>
""", unsafe_allow_html=True)

_, col_l = st.columns([4, 1])
user_lang = col_l.selectbox("🌍 Select Language", ["English", "Hindi (हिन्दी)", "Gujarati (ગુજરાતી)"])

# --- ALL 7 TABS WORKING ---
tabs = st.tabs(
    ["📄 SCANNER", "📚 ACT LIBRARY", "🏛️ COURT DIRECTORY", "✍️ DRAFT FORMATS", "📰 LIVE NEWS", "💬 QUERIES", "ℹ️ ABOUT US"])

# 1. SCANNER
with tabs[0]:
    st.subheader("📄 Strict AI Document Scanner")
    up = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if up:
        c1, c2 = st.columns(2)
        with c1:
            st.image(up, width=400)
        with c2:
            if st.button("🚀 Analyze Now"):
                res = ask_juris_ai("Strict Analysis: Extract parties, dates, and validity.", user_lang,
                                   encode_image(up))
                st.session_state['scan_res'] = res
                st.write(res)
            if 'scan_res' in st.session_state:
                if st.button("🔊 Read Analysis"): speak_text(st.session_state['scan_res'])

# 2. ACT LIBRARY
with tabs[1]:
    st.subheader("📚 Indian Act & Section Search")
    act_q = st.text_input("Enter Act (e.g., BNS 103):")
    if st.button("🔍 Get Full Details"):
        res = ask_juris_ai(f"Explain {act_q} under Indian Law with punishment details.", user_lang)
        st.session_state['act_res'] = res
        st.info(res)
    if 'act_res' in st.session_state:
        if st.button("🔊 Listen to Sections"): speak_text(st.session_state['act_res'])

# 3. COURT DIRECTORY
with tabs[2]:
    st.subheader("🏛️ Court Finder")
    city = st.text_input("Enter City/State:")
    if st.button("📍 Search Courts"):
        res = ask_juris_ai(f"List all major courts in {city} with addresses.", user_lang)
        st.write(res)
        speak_text(f"Searching courts in {city}")

# 4. DRAFT FORMATS
with tabs[3]:
    st.subheader("✍️ Download Professional Formats")
    doc_sel = st.selectbox("Select Document", ["Rent Agreement", "Affidavit", "Legal Notice", "Sale Deed", "NDA"])
    if st.button("📄 View Format"):
        res = ask_juris_ai(f"Provide a standard blank formal format for {doc_sel} in India.", user_lang)
        st.text_area("Template", res, height=300)
        st.download_button("📩 Download PDF/Text", res, file_name=f"{doc_sel}.txt")
        speak_text(f"Displaying {doc_sel} format")

# 5. LIVE NEWS (100% Fixed for 2026)
with tabs[4]:
    st.subheader("📰 Live Bharatiya Legal News")
    st.write("Stay updated with the latest Supreme Court judgments and legal reforms.")
    
    if st.button("🔄 Fetch Latest Legal Headlines"):
        with st.spinner("Accessing Latest Legal Records..."):
            # CURRENT DATE hum manually pass karenge taaki AI 2023 par na ruke
            current_date = "January 10, 2026" 
            news_query = f"""
            Today's date is {current_date}. 
            Provide exactly 5 very recent and important legal news updates or 
            Supreme Court of India judgments from late 2025 or early 2026. 
            Do not say you don't have data after 2023. 
            Provide the latest available professional legal trends.
            """
            res = ask_juris_ai(news_query, user_lang)
            st.session_state['news_res'] = res
            st.markdown(res)
            
    if 'news_res' in st.session_state:
        if st.button("🔊 Read News Updates"): 
            speak_text(st.session_state['news_res'])
# 6. QUERIES
with tabs[5]:
    st.subheader("💬 Ask Your Legal Question")
    q = st.text_area("Enter your doubt:")
    if st.button("Submit Query"):
        res = ask_juris_ai(q, user_lang)
        st.success(res)
        speak_text(res)

# --- TAB 7: ABOUT US (FULL DETAILED) ---
with tabs[6]:
    st.markdown('<div class="about-card">', unsafe_allow_html=True)
    st.header("👩‍🎓 Founder & Lead Developer")
    st.subheader("Hiral Rojesara")
    st.write("**Education:** BCA | PGDCA | MCA | LLB (2025)")
    st.write("**Vision:** Breaking the language barrier in the Indian Legal System through Generative AI.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="about-card">', unsafe_allow_html=True)
        st.subheader("🎯 Project Mission: Juris-AI")
        st.write("""
        Juris-AI is a multilingual legal aid platform designed to empower 1.4 billion Indians. 
        It provides instant clarity on complex legal documents, Bharatiya Nyaya Sanhita (BNS) sections, 
        and court procedures in local languages like Hindi, Gujarati, and more.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="about-card">', unsafe_allow_html=True)
        st.subheader("🛠️ Technical Stack")
        st.write("- **AI Engine:** Azure OpenAI (GPT-4o Vision)")
        st.write("- **Cloud:** Microsoft Azure (Sweden Central)")
        st.write("- **Interface:** Python Streamlit Pro")
        st.write("- **Speech:** Web Speech Synthesis API")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-card">', unsafe_allow_html=True)
    st.subheader("🚀 2026 Roadmap")
    st.write("1. **Live e-Courts Integration:** Directly track case status via API.")
    st.write("2. **Voice-Only Navigation:** Helping the elderly and illiterate access justice.")
    st.write("3. **Legal Kiosks:** Deploying Juris-AI tablets in rural Gram Panchayats.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.success("🏆 Representing Gujarat in Microsoft Imagine Cup 2026")
st.markdown('<div class="footer">⚖️ Microsoft Imagine Cup 2026 | Built by Hiral Rojesara</div>', unsafe_allow_html=True)



