import streamlit as st
from transformers import pipeline

# 1. Page Configuration
st.set_page_config(page_title="Juris-AI Pro | Legal Inclusion", page_icon="⚖️", layout="wide")

# 2. Advanced Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    .stButton>button { border-radius: 20px; }
    .vision-box { padding: 10px; background-color: #e1f5fe; border-radius: 10px; border-left: 5px solid #01579b; margin-bottom: 10px; }
    .founder-card { text-align: center; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Professional Sidebar with Female Icon & Vision
with st.sidebar:
    st.markdown("<div class='founder-card'>", unsafe_allow_html=True)
    # Using a professional female avatar icon
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140047.png", width=120)
    st.subheader("Founder: Hiral Rojesara")
    st.markdown("**BCA + PGDCA + MCA + LLB Scholar**")
    st.markdown("---")

    st.markdown("### 🎯 Startup Vision")
    st.markdown("""
    <div class='vision-box'>
    <b>Mission:</b> To democratize law for 1.4 billion people by breaking language barriers.
    </div>
    <div class='vision-box'>
    <b>Goal:</b> Real-time legal aid in 22+ languages using Azure AI.
    </div>
    """, unsafe_allow_html=True)

    st.info("Goal: SDG 16 - Justice & Strong Institutions")

st.markdown("<h1 style='text-align: center; color: #0078d4;'>⚖️ Juris-AI: Universal Legal Access</h1>",
            unsafe_allow_html=True)

# 4. Tabs with Examples & Reset Options
tab1, tab2, tab3 = st.tabs(["📄 Document Scan (OCR)", "✍️ AI Jargon Simplifier", "🎙️ Voice & Multilingual"])

# --- TAB 1: OCR ---
with tab1:
    st.subheader("Step 1: Upload & Scan")
    st.caption("Example: Upload a Rent Agreement, Court Notice, or Income Certificate.")
    col_file, col_btn = st.columns([4, 1])
    with col_file:
        up_file = st.file_uploader("Drop your file here", type=['pdf', 'jpg', 'png'], key="ocr_file")
    with col_btn:
        if st.button("🔄 Reset Scan"):
            st.rerun()

    if up_file:
        st.success("Analysis in progress using Azure AI...")

# --- TAB 2: AI SIMPLIFIER ---
with tab2:
    st.subheader("Step 2: Simplify Complex Legalese")
    # Example Text for User
    st.markdown("**Example:** *'The party of the first part shall be estopped from any further claims...'*")

    text_input = st.text_area("Paste Legal Text:", height=200, key="jargon_text")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        analyze_btn = st.button("🚀 Analyze & Simplify")
    with c2:
        if st.button("🗑️ Clear Input"):
            st.rerun()

    if analyze_btn and text_input:
        with st.spinner('Decoding...'):
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            result = summarizer(text_input, max_length=100, min_length=20)
            st.success(f"**Simplified:** {result[0]['summary_text']}")

# --- TAB 3: VOICE ---
with tab3:
    st.subheader("Step 3: Inclusive Accessibility")
    st.write("**Example:** Select 'Hindi' to hear the summary in your regional language.")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.selectbox("Target Language", ["Hindi", "Gujarati", "Tamil", "Marathi", "Bengali"])
        st.button("🎤 Start Mic")
    with col_v2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("🔊 Play Audio Summary")

st.divider()
st.caption("Built for Microsoft Imagine Cup 2026 | Bridge the Justice Gap")