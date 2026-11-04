"""
Writing Assistant Studio - Consumer-Grade AI Writing Workspace.
Inspired by Notion AI, DeepL, and Grammarly.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import html
import streamlit as st
from utils.ui_utils import inject_consumer_css
from config.settings import SAMPLE_INPUTS
from services.pipeline_service import PipelineService

# Page Setup
st.set_page_config(
    page_title="Hinglish AI Studio | Smart Writing Assistant",
    page_icon="✨",
    layout="wide"
)

inject_consumer_css()

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

# Top Brand Header Bar
st.markdown("""
<div class="brand-nav">
    <div class="brand-title-wrap">
        <div class="brand-logo">✨</div>
        <div>
            <h1 class="brand-text-title">HINGLISH AI STUDIO</h1>
            <div style="font-size: 0.78rem; color: #94A3B8;">Next-Gen Indian Language Transliteration & Writing Assistant</div>
        </div>
    </div>
    <div style="display: flex; gap: 0.5rem; align-items: center;">
        <span class="pill pill-indigo">IndicXlit</span>
        <span class="pill pill-purple">Param-1</span>
        <span class="pill pill-emerald">IndicTrans2</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Preset Chips Toolbar
st.markdown("##### ⚡ Quick Try Examples")

chip_col1, chip_col2, chip_col3, chip_col4, chip_col5 = st.columns(5)

with chip_col1:
    if st.button("🏢 Office & Commute", use_container_width=True):
        st.session_state.input_text = "Mujhe aaj office jana hai"
        st.rerun()

with chip_col2:
    if st.button("🎓 College & Class", use_container_width=True):
        st.session_state.input_text = "kal hamari data science ki class kitne baje shuru hogi?"
        st.rerun()

with chip_col3:
    if st.button("☕ Casual Conversation", use_container_width=True):
        st.session_state.input_text = "bhai kal sham ko chai peene chalte hai."
        st.rerun()

with chip_col4:
    if st.button("📄 Project Submission", use_container_width=True):
        st.session_state.input_text = "kripya project report ki pdf file jaldi bhej dijiye."
        st.rerun()

with chip_col5:
    if st.button("🤖 AI Explanation", use_container_width=True):
        st.session_state.input_text = "hum artificial intelligence aur natural language processing ka use karke ek smart writing assistant bana rahe hai."
        st.rerun()

# 2-Column Consumer Workspace (Left: Input Canvas, Right: Output Canvas)
col_editor, col_output = st.columns([1, 1], gap="large")

with col_editor:
    st.markdown("""
    <div class="editor-header">
        <span class="editor-header-title">
            <span>✍️</span> Roman Hinglish Input
        </span>
        <span class="pill pill-slate">QWERTY Keyboard</span>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        label="Input Text Area",
        value=st.session_state.input_text,
        height=210,
        placeholder="Type in Roman script, e.g. 'Mujhe aaj office jana hai' or 'Aap kaise ho?'...",
        label_visibility="collapsed"
    )
    st.session_state.input_text = user_input

    # Input Stats & Clear Row
    input_char_cnt = len(user_input)
    input_word_cnt = len(user_input.split()) if user_input.strip() else 0

    c_stat1, c_stat2 = st.columns([2, 1])
    with c_stat1:
        st.caption(f"📊 `{input_word_cnt}` words · `{input_char_cnt}` characters")
    with c_stat2:
        if st.button("🗑️ Clear Input", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.xlit_output = ""
            st.session_state.improved_output = ""
            st.session_state.trans_output = ""
            st.session_state.last_latency = None
            st.rerun()

    # Action Toolbar
    st.markdown("##### 🚀 Execution Actions")
    col_act1, col_act2 = st.columns([1.6, 1])

    with col_act1:
        btn_transform = st.button("⚡ Transform All (End-to-End)", type="primary", use_container_width=True)

    with col_act2:
        btn_xlit_only = st.button("🔤 Transliterate", use_container_width=True)

    col_act3, col_act4 = st.columns(2)
    with col_act3:
        btn_enhance_only = st.button("✨ Polish Hindi", use_container_width=True)
    with col_act4:
        btn_trans_only = st.button("🌐 Translate English", use_container_width=True)

# Execution Triggers
if btn_transform:
    if not user_input.strip():
        st.warning("Please type or choose a Hinglish sentence above.")
    else:
        with st.spinner("Processing through AI4Bharat & BharatGen Neural Pipeline..."):
            res = pipeline.process_all(user_input, apply_enhancement=True)
            if res["success"]:
                st.session_state.xlit_output = res["transliterated_hindi"]
                st.session_state.improved_output = res["improved_hindi"]
                st.session_state.trans_output = res["english_translation"]
                st.session_state.last_latency = res["total_latency_ms"]
                st.toast(f"Transformed in {res['total_latency_ms']} ms!", icon="✨")
                st.rerun()
            else:
                st.error(f"Error: {res.get('error')}")

elif btn_xlit_only:
    if not user_input.strip():
        st.warning("Please enter Hinglish text.")
    else:
        with st.spinner("Transliterating with AI4Bharat IndicXlit..."):
            res = pipeline.xlit.transliterate(user_input)
            if res["success"]:
                st.session_state.xlit_output = res["devanagari_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Transliterated in {res['latency_ms']} ms", icon="🔤")
                st.rerun()
            else:
                st.error(res.get("error"))

elif btn_enhance_only:
    src_hindi = st.session_state.xlit_output or user_input
    if not src_hindi.strip():
        st.warning("Please transliterate text first.")
    else:
        with st.spinner("Polishing grammar with BharatGen Param-1..."):
            res = pipeline.writing.improve_writing(src_hindi)
            if res["success"]:
                st.session_state.improved_output = res["improved_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Polished in {res['latency_ms']} ms", icon="✨")
                st.rerun()
            else:
                st.error(res.get("error"))

elif btn_trans_only:
    src_hindi = st.session_state.improved_output or st.session_state.xlit_output or user_input
    if not src_hindi.strip():
        st.warning("Please provide Hindi text to translate.")
    else:
        with st.spinner("Translating with AI4Bharat IndicTrans2..."):
            res = pipeline.translation.translate(src_hindi)
            if res["success"]:
                st.session_state.trans_output = res["english_text"]
                st.session_state.last_latency = res["latency_ms"]
                st.toast(f"Translated in {res['latency_ms']} ms", icon="🌐")
                st.rerun()
            else:
                st.error(res.get("error"))

# Right Column: Output Studio
with col_output:
    st.markdown("""
    <div class="editor-header">
        <span class="editor-header-title">
            <span>🎯</span> Generated Output Studio
        </span>
        <span class="pill pill-purple">AI Augmented</span>
    </div>
    """, unsafe_allow_html=True)

    tab_polished, tab_trans, tab_raw_xlit, tab_grid = st.tabs([
        "✨ Polished Hindi",
        "🌐 English Translation",
        "🔤 Native Script",
        "🔍 4-Way Comparison"
    ])

    with tab_polished:
        enhanced_text = st.session_state.improved_output or st.session_state.xlit_output or ""
        escaped_enhanced = html.escape(enhanced_text) if enhanced_text else '<span style="color:#64748B; font-style:italic;">Transformed text will appear here...</span>'

        st.markdown(f"""
        <div class="hero-output-box">
            <div class="hero-output-header">
                <span class="hero-output-title">
                    <span>✨</span> Enhanced Devanagari Hindi
                </span>
                <span class="pill pill-purple">BharatGen Param-1</span>
            </div>
            <div class="hero-devanagari-text">{escaped_enhanced}</div>
        </div>
        """, unsafe_allow_html=True)

        if enhanced_text:
            col_c1, col_c2 = st.columns([1, 2])
            with col_c1:
                st.button("📋 Copy Enhanced Hindi", key="copy_hero_enhanced", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard!", icon="✅"))
            with col_c2:
                st.caption("Grammar, matras, and punctuation verified.")

    with tab_trans:
        trans_text = st.session_state.trans_output or ""
        escaped_trans = html.escape(trans_text) if trans_text else '<span style="color:#64748B; font-style:italic;">Translation will appear here...</span>'

        st.markdown(f"""
        <div class="hero-output-box">
            <div class="hero-output-header">
                <span class="hero-output-title">
                    <span>🌐</span> Natural English Translation
                </span>
                <span class="pill pill-emerald">AI4Bharat IndicTrans2</span>
            </div>
            <div class="hero-english-text">{escaped_trans}</div>
        </div>
        """, unsafe_allow_html=True)

        if trans_text:
            col_t1, col_t2 = st.columns([1, 2])
            with col_t1:
                st.button("📋 Copy English Translation", key="copy_hero_trans", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard!", icon="✅"))
            with col_t2:
                st.caption("Idiomatic English translation with preserved meaning.")

    with tab_raw_xlit:
        raw_xlit_text = st.session_state.xlit_output or ""
        escaped_raw = html.escape(raw_xlit_text) if raw_xlit_text else '<span style="color:#64748B; font-style:italic;">Transliteration will appear here...</span>'

        st.markdown(f"""
        <div class="hero-output-box">
            <div class="hero-output-header">
                <span class="hero-output-title">
                    <span>🔤</span> Raw Native Transliteration
                </span>
                <span class="pill pill-indigo">AI4Bharat IndicXlit</span>
            </div>
            <div class="hero-devanagari-text">{escaped_raw}</div>
        </div>
        """, unsafe_allow_html=True)

        if raw_xlit_text:
            st.button("📋 Copy Native Script", key="copy_hero_raw", use_container_width=True, on_click=lambda: st.toast("Copied to clipboard!", icon="✅"))

    with tab_grid:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(f"""
            <div class="compare-card">
                <div class="compare-card-top">
                    <span class="compare-label">1. Original Input</span>
                    <span class="pill pill-slate">Hinglish</span>
                </div>
                <div class="compare-body">{html.escape(st.session_state.input_text or "No input")}</div>
            </div>
            """, unsafe_allow_html=True)

        with g2:
            st.markdown(f"""
            <div class="compare-card">
                <div class="compare-card-top">
                    <span class="compare-label">2. IndicXlit</span>
                    <span class="pill pill-indigo">Native</span>
                </div>
                <div class="compare-body compare-body-hindi">{html.escape(st.session_state.xlit_output or "Pending")}</div>
            </div>
            """, unsafe_allow_html=True)

        g3, g4 = st.columns(2)
        with g3:
            st.markdown(f"""
            <div class="compare-card" style="margin-top: 1rem;">
                <div class="compare-card-top">
                    <span class="compare-label">3. Param-1 Polish</span>
                    <span class="pill pill-purple">Enhanced</span>
                </div>
                <div class="compare-body compare-body-hindi">{html.escape(st.session_state.improved_output or "Pending")}</div>
            </div>
            """, unsafe_allow_html=True)

        with g4:
            st.markdown(f"""
            <div class="compare-card" style="margin-top: 1rem;">
                <div class="compare-card-top">
                    <span class="compare-label">4. IndicTrans2</span>
                    <span class="pill pill-emerald">English</span>
                </div>
                <div class="compare-body">{html.escape(st.session_state.trans_output or "Pending")}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.last_latency:
        st.markdown(f"<div style='text-align: right; margin-top: 0.8rem; font-size: 0.82rem; color: #64748B;'>⚡ Pipeline latency: <span style='color: #10B981; font-weight: 700;'>{st.session_state.last_latency} ms</span></div>", unsafe_allow_html=True)
