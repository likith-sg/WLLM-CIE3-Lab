"""
HINGLISH AI - Intelligent Indian Language Transliteration, Writing Enhancement and Translation System.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
Main Application Entrypoint (Home Page).
"""

import streamlit as st
from utils.ui_utils import inject_consumer_css
from utils.model_utils import get_gpu_memory_info, safe_device
from config.settings import (
    INDICXLIT_MODEL_ID,
    INDICTRANS2_MODEL_ID,
    PARAM1_MODEL_ID
)

# Page configuration
st.set_page_config(
    page_title="HINGLISH AI | Smart Writing Assistant",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_consumer_css()

# Sidebar Information
with st.sidebar:
    st.markdown("### 🇮🇳 HINGLISH AI")
    st.caption("CS3235 CIE3 Mini Project")
    st.markdown("---")
    
    st.markdown("#### ⚡ Hardware Status")
    device = safe_device()
    gpu_info = get_gpu_memory_info()
    if gpu_info.get("available"):
        st.success(f"**GPU:** {gpu_info.get('name')}")
        st.write(f"**VRAM Total:** {gpu_info.get('total_gb')} GB")
        st.write(f"**Free VRAM:** {gpu_info.get('free_gb')} GB")
    else:
        st.info("**Compute Device:** CPU Execution (Safe Mode)")

    st.markdown("---")
    st.markdown("#### 🏛️ Academic Attributions")
    st.markdown("- **AI4Bharat:** IndicXlit & IndicTrans2")
    st.markdown("- **BharatGen:** Param-1 LLM")
    st.markdown("- **IIT Madras:** Aksharantar Benchmark")

# Main Content Hero
st.markdown('<div class="hero-badge">AI4Bharat + BharatGen Research Foundation</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Hinglish Smart Writing Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">From the way you type to the way you express. Bridge colloquial Roman Hinglish with native Devanagari Hindi, generative styling, and natural English translation.</p>', unsafe_allow_html=True)

# Call to Action
col_cta1, col_cta2 = st.columns([1, 4])
with col_cta1:
    if st.button("🚀 Launch Studio", type="primary", use_container_width=True):
        st.switch_page("pages/1_Writing_Assistant.py")
with col_cta2:
    if st.button("📊 Open Evaluation Dashboard", use_container_width=True):
        st.switch_page("pages/2_Evaluation.py")

st.markdown("---")

# Feature Highlights Grid
st.markdown("### 🌟 Core Capabilities")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="studio-card">
        <div class="card-header">
            <span class="card-title">1. Transliteration</span>
            <span class="card-badge badge-xlit">AI4Bharat IndicXlit</span>
        </div>
        <div class="card-content">
            Converts phonetically typed Roman Hinglish into flawless native Devanagari Hindi while preserving punctuation, numbers, and technical terms.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="studio-card">
        <div class="card-header">
            <span class="card-title">2. AI Enhancement</span>
            <span class="card-badge badge-enhance">BharatGen Param-1</span>
        </div>
        <div class="card-content">
            Refines sentence flow, rectifies subject-verb agreement, fixes colloquial matra slips, and elevates readability while strictly preserving meaning.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="studio-card">
        <div class="card-header">
            <span class="card-title">3. Neural Translation</span>
            <span class="card-badge badge-trans">AI4Bharat IndicTrans2</span>
        </div>
        <div class="card-content">
            Translates the Devanagari output into idiomatic, grammatically sound English with high semantic accuracy and preservation of colloquial tone.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Pipeline Architecture Walkthrough
st.markdown("### 🔄 Multi-Stage Processing Pipeline")
st.markdown("""
```mermaid
graph LR
    A["Roman Hinglish Input<br/><i>'mera naam likith hai aur mai bangalore me rehta hu'</i>"] --> B["AI4Bharat IndicXlit<br/><b>Transliteration</b>"]
    B --> C["Devanagari Hindi<br/><i>मेरा नाम लिखित है और मैं बैंगलोर में रहता हूँ</i>"]
    C --> D["BharatGen Param-1<br/><b>Generative Polish</b>"]
    D --> E["Enhanced Hindi<br/><i>मेरा नाम लिखित है और मैं बैंगलोर में रहता हूँ।</i>"]
    E --> F["AI4Bharat IndicTrans2<br/><b>Machine Translation</b>"]
    F --> G["English Output<br/><i>My name is Likith and I live in Bangalore.</i>"]
```
""", unsafe_allow_html=True)

st.markdown("---")

# Model Metadata Specifications
st.markdown("### 🧠 Foundation Model Inventory")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown("**AI4Bharat IndicXlit**")
    st.caption("Primary Transliteration Model")
    st.code(f"ID: {INDICXLIT_MODEL_ID}\nFormat: Seq2Seq / Phonetic\nTarget: Roman -> Devanagari\nLicense: MIT / Open Academic")

with col_m2:
    st.markdown("**BharatGen Param-1**")
    st.caption("Generative Writing Enhancement")
    st.code(f"ID: {PARAM1_MODEL_ID}\nArchitecture: 2.9B Causal LM\nOptimization: 4-bit / CPU Offload\nOrganization: bharatgenai")

with col_m3:
    st.markdown("**AI4Bharat IndicTrans2**")
    st.caption("Primary Translation Model")
    st.code(f"ID: {INDICTRANS2_MODEL_ID}\nArchitecture: Distilled 200M Transformer\nDirection: hin_Deva -> eng_Latn\nLicense: MIT / Open Research")

st.markdown("""
<div class="app-footer">
    CS3235 Individual Undergraduate Mini Project • Designed and Developed for CIE3 Assessment • November 2026
</div>
""", unsafe_allow_html=True)
