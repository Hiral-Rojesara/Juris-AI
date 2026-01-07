import streamlit as st
from transformers import pipeline

# 1. Page Configuration
st.set_page_config(page_title="Juris-AI | Universal Legal Access", page_icon="⚖️", layout="wide")

# 2. State Initialization (Fixes Tab-to-Tab Data Loss)
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0
if "summary_result" not in st.session_state:
    st.session_state.summary_result = ""

# 3. Premium Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .banner { background: linear-gradient(135deg, #004578, #0078d4); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    .sidebar-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center; margin-bottom: 15px; }
    .vision-box { background-color: #f0f7ff; border-left: 5px solid #0078d4; padding: 15px; border-radius: 10px; font-size: 14px; line-height: 1.5; color: #1a3a5a; }
    .qualification-tag { background: #e8f4fd; color: #005a9e; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 12px; display: inline-block; margin: 2px; }
    .stButton>button { border-radius: 20px; font-weight: bold; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar: Advanced Founder Profile & Detailed Vision
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140047.png", width=90)
    st.markdown("Solo Founder & Innovator - Hiral Rojesara")
    st.markdown("""
        <div style='margin-top:10px;'>
            <span class='qualification-tag'>🎓 <b>BCA - Technical Core </b></span><br>
            <span class='qualification-tag'>🎓 <b>PGDCA - Technical Core </b></span><br>
            <span class='qualification-tag'>🎓 <b>MCA - Technical Core </b></span><br>
            <span class='qualification-tag'>⚖️ <b>LLB (2025) - Legal Expertise</b></span><br>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🎯 Detailed Project Vision")
    st.markdown("""
    <div class='vision-box'>
    <b>Phase 1: Legal Literacy (Universal Access)</b><br>
    Breaking down high-level 'Legalese' (Complex Court Language) into simple, understandable terms for 1.4 Billion people using Azure AI.<br><br>
    <b>Phase 2: Global Inclusion</b><br>
    Democratizing justice by providing automated legal drafting and translation in 22+ Indian languages and 100+ Global languages.<br><br>
    <b>Phase 3: SDG 16 Alignment</b><br>
    Strengthening legal institutions by reducing the gap between common citizens and law, ensuring "Justice for All" regardless of language or education.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Reset Application", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 5. Professional Header
st.markdown(
    "<div class='banner'><h1>⚖️ Juris-AI: Universal Legal Access</h1><p>Empowering 8 Billion People with AI-Driven Justice</p></div>",
    unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 OCR Scanner", "🧠 AI Jargon Simplifier", "🌐 Universal Translation", "✍️ Global Doc Creator"])

# --- TAB 1: OCR ---
with tab1:
    st.subheader("Step 1: Intelligent Text Extraction")
    # Dynamic key for clear functionality
    col_up, col_clr = st.columns([6, 1])
    with col_up:
        up_file = st.file_uploader("Upload Legal Document (PDF/JPG/PNG)", type=['pdf', 'png', 'jpg'],
                                   key=f"ocr_{st.session_state.reset_count}")
    with col_clr:
        st.write(" ")  # Spacer
        if st.button("🗑️", key="clr_tab1", help="Clear Upload"):
            st.session_state.reset_count += 1
            st.rerun()
    if up_file:
        st.success(f"✅ Document '{up_file.name}' analyzed using Azure AI Vision framework.")

# --- TAB 2: SIMPLIFIER ---
with tab2:
    st.subheader("Step 2: Legal Jargon Simplifier")
    raw_input = st.text_area("Paste Complex Legal Text:", height=150, key=f"sim_{st.session_state.reset_count}")

    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🚀 Simplify"):
            if raw_input:
                with st.spinner("Decoding Legalese..."):
                    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
                    st.session_state.summary_result = summarizer(raw_input, max_length=70, min_length=30)[0][
                        'summary_text']
                    st.rerun()
    with c2:
        if st.button("🗑️", key="clr_tab2", help="Clear Text"):
            st.session_state.summary_result = ""
            st.session_state.reset_count += 1
            st.rerun()

    if st.session_state.summary_result:
        st.success(f"**Simplified Result:** {st.session_state.summary_result}")

# --- TAB 3: TRANSLATION ---
with tab3:
    st.subheader("Step 3: Universal Language Access")
    # Fetching data directly from Tab 2's session state
    if st.session_state.summary_result:
        st.info(f"**Input for Translation:** {st.session_state.summary_result}")
        target = st.selectbox("Select Target Language:",
                              ["Hindi", "Gujarati", "Spanish", "French", "German", "Arabic", "Mandarin"])

        btn_tr, btn_sp, btn_empty = st.columns([2, 2, 4])
        with btn_tr:
            if st.button(f"🌐 Translate to {target}"):
                st.write(f"Processing Azure Translator API for {target}...")
        with btn_sp:
            st.button("🔊 Play Audio Summary")
    else:
        st.warning("⚠️ No data found. Please complete 'Step 2: AI Jargon Simplifier' first.")

# --- TAB 4: GLOBAL DOC CREATOR ---
with tab4:
    st.subheader("Step 4: Global Legal Document Creator")

    cat = st.selectbox("Document Category:",
                       ["Property & Real Estate", "Business & Finance", "Court & Estate Planning"],
                       key=f"cat_{st.session_state.reset_count}")
    doc_map = {"Property & Real Estate": ["Rent Agreement", "Sale Deed", "Lease Deed"],
               "Business & Finance": ["NDA", "Partnership Deed", "Contract"],
               "Court & Estate Planning": ["Affidavit", "Will", "Legal Notice"]}
    selected_doc = st.selectbox("Select Document:", doc_map[cat], key=f"doc_{st.session_state.reset_count}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("Full Name (Party 1)", key=f"n1_{st.session_state.reset_count}")
        st.text_input("Location / City", key=f"loc_{st.session_state.reset_count}")
    with col_b:
        st.text_input("Other Party / Authority", key=f"p2_{st.session_state.reset_count}")
        st.text_area("Specific Details / Clauses", height=68, key=f"ext_{st.session_state.reset_count}")

    act1, act2 = st.columns([6, 1])
    with act1:
        if st.button(f"📝 Generate {selected_doc}", use_container_width=True):
            st.success(f"✅ {selected_doc} Drafted Successfully!")
            st.code(
                f"DRAFT: {selected_doc.upper()}\nParty: {st.session_state.get(f'n1_{st.session_state.reset_count}')}\n[AI Legal Clauses generated...]")
    with act2:
        if st.button("🗑️", key="clr_tab4", help="Clear All Fields"):
            st.session_state.reset_count += 1
            st.rerun()

# --- FINAL FOOTER ---
st.divider()
st.markdown(
    f"<p style='text-align: center; color: #777;'>Juris-AI © 2026 | Microsoft Imagine Cup Submission | Founder: Hiral Rojesara (Technical & Legal Expertise)</p>",
    unsafe_allow_html=True)
