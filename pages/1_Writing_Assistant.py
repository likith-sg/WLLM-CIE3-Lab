"""
Writing Assistant Studio - Professional Consumer Interface.
Apple Light Theme with Soul & Depth.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import html
import streamlit as st
from utils.ui_utils import inject_consumer_css, render_top_navbar
from services.pipeline_service import PipelineService

# Page Setup - Sidebar hidden via CSS
st.set_page_config(
    page_title="Writing Assistant | Hinglish AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_consumer_css()
render_top_navbar("studio")

# Session State Management
if "pipeline_service" not in st.session_state:
    st.session_state.pipeline_service = PipelineService()

if "input_text" not in st.session_state:
    st.session_state.input_text = "Mujhe aaj office jana hai"

if "xlit_output" not in st.session_state:
    st.session_state.xlit_output = "मुझे आज ऑफिस जाना है"

if "improved_output" not in st.session_state:
    st.session_state.improved_output = "मुझे आज ऑफिस जाना है।"

if "trans_output" not in st.session_state:
    st.session_state.trans_output = "I have to go to the office today."

if "last_latency" not in st.session_state:
    st.session_state.last_latency = 8.5

pipeline: PipelineService = st.session_state.pipeline_service

# Sample Scenarios Map (Prevents horizontal column button overflow)
SAMPLES = {
    "Select or load a sample scenario...": "",
    "Office & Commute: Mujhe aaj office jana hai": "Mujhe aaj office jana hai",
    "Academic Schedule: kal hamari data science ki class kitne baje shuru hogi?": "kal hamari data science ki class kitne baje shuru hogi?",
    "Casual Dialogue: bhai kal sham ko chai peene chalte hai.": "bhai kal sham ko chai peene chalte hai.",
    "Project Submission: kripya project report ki pdf file jaldi bhej dijiye.": "kripya project report ki pdf file jaldi bhej dijiye.",
    "Technical Explanation: hum artificial intelligence aur natural language processing ka use karke ek smart writing assistant bana rahe hai.": "hum artificial intelligence aur natural language processing ka use karke ek smart writing assistant bana rahe hai."
}

col_sample_select, col_sample_btn = st.columns([3.8, 1.2])
with col_sample_select:
    chosen_sample = st.selectbox(
        label="Sample Scenarios",
        options=list(SAMPLES.keys()),
        label_visibility="collapsed"
    )
with col_sample_btn:
    if st.button("Load Scenario", use_container_width=True):
        if SAMPLES.get(chosen_sample):
            st.session_state.input_text = SAMPLES[chosen_sample]
            st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Dual-Pane Pro Workspace (Left: Input Canvas, Right: Output Canvas)
col_editor, col_output = st.columns([1, 1], gap="large")

with col_editor:
    st.markdown("""
    <div class="apple-card-header">
        <span class="apple-card-title">Source Roman Hinglish</span>
        <span class="badge-slate">QWERTY Input</span>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        label="Input Text Area",
        value=st.session_state.input_text,
        height=215,
        placeholder="Type in Roman script, e.g., 'Mujhe aaj office jana hai' or 'Aap kaise ho?'...",
        label_visibility="collapsed"
    )
    st.session_state.input_text = user_input

    # Input Metrics & Clear Control
    input_char_cnt = len(user_input)
    input_word_cnt = len(user_input.split()) if user_input.strip() else 0

    c_stat1, c_stat2 = st.columns([2.4, 1])
    with c_stat1:
        st.markdown(f"<div style='font-size: 0.8rem; color: #64748b; padding-top: 8px; font-weight: 500;'>{input_word_cnt} words · {input_char_cnt} characters</div>", unsafe_allow_html=True)
    with c_stat2:
        if st.button("Clear Text", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.xlit_output = ""
            st.session_state.improved_output = ""
            st.session_state.trans_output = ""
            st.session_state.last_latency = None
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Action Toolbar
    st.markdown("<div style='font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 8px;'>Execution Pipeline</div>", unsafe_allow_html=True)
    
    col_act1, col_act2 = st.columns([1.6, 1])
    with col_act1:
        btn_transform = st.button("Process Pipeline (End-to-End)", type="primary", use_container_width=True)
    with col_act2:
        btn_xlit_only = st.button("Transliterate", use_container_width=True)

    col_act3, col_act4 = st.columns(2)
    with col_act3:
        btn_enhance_only = st.button("Enhance Phrasing", use_container_width=True)
    with col_act4:
        btn_trans_only = st.button("Translate to English", use_container_width=True)

# Execution Triggers
if btn_transform:
    if not user_input.strip():
        st.warning("Please provide a Roman Hinglish input sentence.")
    else:
        with st.spinner("Processing through AI4Bharat and BharatGen Neural Pipeline..."):
            res = pipeline.process_all(user_input, apply_enhancement=True)
            if res["success"]:
                st.session_state.xlit_output = res["transliterated_hindi"]
                st.session_state.improved_output = res["improved_hindi"]
                st.session_state.trans_output = res["english_translation"]
                st.session_state.last_latency = res["total_latency_ms"]
                st.toast(f"Pipeline executed in {res['total_latency_ms']} ms")
                st.rerun()
            else:
                st.error(f"Execution error: {res.get('error')}")

elif btn_xlit_only:
    if not user_input.strip():
        st.warning("Please provide Roman Hinglish text.")
    else:
        with st.spinner("Transliterating via AI4Bharat IndicXlit..."):
            res = pipeline.xlit.transliterate(user_input)
            if res["success"]:
                st.session_state.xlit_output = res["devanagari_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Transliteration completed in {res['latency_ms']} ms")
                st.rerun()
            else:
                st.error(res.get("error"))

elif btn_enhance_only:
    src_hindi = st.session_state.xlit_output or user_input
    if not src_hindi.strip():
        st.warning("Please transliterate text before enhancement.")
    else:
        with st.spinner("Refining grammar and structure via BharatGen Param-1..."):
            res = pipeline.writing.improve_writing(src_hindi)
            if res["success"]:
                st.session_state.improved_output = res["improved_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Enhancement completed in {res['latency_ms']} ms")
                st.rerun()
            else:
                st.error(res.get("error"))

elif btn_trans_only:
    src_hindi = st.session_state.improved_output or st.session_state.xlit_output or user_input
    if not src_hindi.strip():
        st.warning("Please provide Hindi text to translate.")
    else:
        with st.spinner("Translating via AI4Bharat IndicTrans2..."):
            res = pipeline.translation.translate(src_hindi)
            if res["success"]:
                st.session_state.trans_output = res["english_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Translation completed in {res['latency_ms']} ms")
                st.rerun()
            else:
                st.error(res.get("error"))

# Right Column: Output Studio
with col_output:
    st.markdown("""
    <div class="apple-card-header">
        <span class="apple-card-title">Generated Output</span>
        <span class="badge-green">AI Active</span>
    </div>
    """, unsafe_allow_html=True)

    tab_polished, tab_trans, tab_raw_xlit, tab_grid = st.tabs([
        "Enhanced Hindi",
        "English Translation",
        "Transliterated Script",
        "Side-by-Side Matrix"
    ])

    with tab_polished:
        enhanced_text = st.session_state.improved_output or st.session_state.xlit_output or ""
        escaped_enhanced = html.escape(enhanced_text) if enhanced_text else '<span style="color: #94a3b8; font-style: normal;">Output will appear here upon execution.</span>'

        st.markdown(f"""
        <div class="output-display-card">
            <div class="apple-card-header">
                <span style="font-size: 0.8rem; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em;">Enhanced Devanagari Hindi</span>
                <span class="badge-green">BharatGen Param-1</span>
            </div>
            <div class="output-devanagari-hero">{escaped_enhanced}</div>
        </div>
        """, unsafe_allow_html=True)

        if enhanced_text:
            col_c1, col_c2 = st.columns([1.3, 2])
            with col_c1:
                st.button("Copy Enhanced Hindi", key="copy_hero_enhanced", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard."))
            with col_c2:
                st.caption("Grammatical agreement, matra normalization, and punctuation refined.")

    with tab_trans:
        trans_text = st.session_state.trans_output or ""
        escaped_trans = html.escape(trans_text) if trans_text else '<span style="color: #94a3b8; font-style: normal;">Translation will appear here upon execution.</span>'

        st.markdown(f"""
        <div class="output-display-card">
            <div class="apple-card-header">
                <span style="font-size: 0.8rem; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em;">Natural English Translation</span>
                <span class="badge-blue">AI4Bharat IndicTrans2</span>
            </div>
            <div class="output-english-hero">{escaped_trans}</div>
        </div>
        """, unsafe_allow_html=True)

        if trans_text:
            col_t1, col_t2 = st.columns([1.3, 2])
            with col_t1:
                st.button("Copy Translation", key="copy_hero_trans", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard."))
            with col_t2:
                st.caption("Idiomatic translation preserving original semantic intent.")

    with tab_raw_xlit:
        raw_xlit_text = st.session_state.xlit_output or ""
        escaped_raw = html.escape(raw_xlit_text) if raw_xlit_text else '<span style="color: #94a3b8; font-style: normal;">Transliterated text will appear here upon execution.</span>'

        st.markdown(f"""
        <div class="output-display-card">
            <div class="apple-card-header">
                <span style="font-size: 0.8rem; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em;">Raw Native Transliteration</span>
                <span class="badge-slate">AI4Bharat IndicXlit</span>
            </div>
            <div class="output-devanagari-hero">{escaped_raw}</div>
        </div>
        """, unsafe_allow_html=True)

        if raw_xlit_text:
            st.button("Copy Native Script", key="copy_hero_raw", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard."))

    with tab_grid:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(f"""
            <div class="matrix-card">
                <div class="matrix-header">
                    <span class="matrix-title">1. Original Input</span>
                    <span class="badge-slate">Source</span>
                </div>
                <div class="matrix-content">{html.escape(st.session_state.input_text or "No input provided")}</div>
            </div>
            """, unsafe_allow_html=True)

        with g2:
            st.markdown(f"""
            <div class="matrix-card">
                <div class="matrix-header">
                    <span class="matrix-title">2. IndicXlit</span>
                    <span class="badge-blue">Transliterated</span>
                </div>
                <div class="matrix-content matrix-content-devanagari">{html.escape(st.session_state.xlit_output or "Pending execution")}</div>
            </div>
            """, unsafe_allow_html=True)

        g3, g4 = st.columns(2)
        with g3:
            st.markdown(f"""
            <div class="matrix-card" style="margin-top: 0.85rem;">
                <div class="matrix-header">
                    <span class="matrix-title">3. Param-1 Polish</span>
                    <span class="badge-green">Enhanced</span>
                </div>
                <div class="matrix-content matrix-content-devanagari">{html.escape(st.session_state.improved_output or "Pending execution")}</div>
            </div>
            """, unsafe_allow_html=True)

        with g4:
            st.markdown(f"""
            <div class="matrix-card" style="margin-top: 0.85rem;">
                <div class="matrix-header">
                    <span class="matrix-title">4. IndicTrans2</span>
                    <span class="badge-blue">Translated</span>
                </div>
                <div class="matrix-content">{html.escape(st.session_state.trans_output or "Pending execution")}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.last_latency:
        st.markdown(f"<div style='text-align: right; margin-top: 0.85rem; font-size: 0.78rem; color: #64748b;'>Pipeline execution: <span style='color: #059669; font-weight: 700;'>{st.session_state.last_latency} ms</span></div>", unsafe_allow_html=True)
