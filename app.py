"""
Hinglish Smart Writing Assistant - Indian Language Transliteration, Writing Enhancement and Translation.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
Main Application Entrypoint.
"""

import streamlit as st
from utils.ui_utils import inject_consumer_css, render_top_navbar
from utils.model_utils import get_gpu_memory_info, safe_device
from config.settings import (
    INDICXLIT_MODEL_ID,
    INDICTRANS2_MODEL_ID,
    PARAM1_MODEL_ID
)

# Page configuration - Light theme
st.set_page_config(
    page_title="Hinglish Smart Writing Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_consumer_css()
render_top_navbar("overview")

# Main Content Hero
st.markdown('<div class="badge-green" style="display: inline-block; margin-bottom: 0.75rem;">AI4Bharat & BharatGen Foundation Models</div>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 2.75rem; font-weight: 700; letter-spacing: -0.035em; color: #0f172a; margin-bottom: 0.5rem; line-height: 1.1;">Hinglish Smart Writing Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.15rem; color: #475569; max-width: 820px; line-height: 1.5; margin-bottom: 1.75rem;">An autonomous system designed to bridge informal Roman-script Hinglish with native Devanagari Hindi, refine grammatical phrasing with generative foundation models, and translate into natural English.</p>', unsafe_allow_html=True)

# Call to Action
col_cta1, col_cta2, col_spacer = st.columns([1.3, 1.8, 3])
with col_cta1:
    if st.button("Launch Studio", type="primary", use_container_width=True):
        st.switch_page("pages/1_Writing_Assistant.py")
with col_cta2:
    if st.button("Evaluation Benchmark", use_container_width=True):
        st.switch_page("pages/2_Evaluation.py")

st.markdown("---")

# Feature Highlights Grid
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Core Capabilities</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="apple-card">
        <div class="apple-card-header">
            <span class="apple-card-title">1. Transliteration</span>
            <span class="badge-blue">AI4Bharat IndicXlit</span>
        </div>
        <div style="font-size: 0.92rem; color: #475569; line-height: 1.55;">
            Converts phonetically typed Roman Hinglish into native Devanagari Hindi while preserving numbers, technical loanwords, and punctuation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="apple-card">
        <div class="apple-card-header">
            <span class="apple-card-title">2. Generative Polish</span>
            <span class="badge-green">BharatGen Param-1</span>
        </div>
        <div style="font-size: 0.92rem; color: #475569; line-height: 1.55;">
            Rectifies subject-verb agreement, normalizes matras and diacritics, and elevates sentence readability while strictly preserving factual meaning.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="apple-card">
        <div class="apple-card-header">
            <span class="apple-card-title">3. Neural Translation</span>
            <span class="badge-blue">AI4Bharat IndicTrans2</span>
        </div>
        <div style="font-size: 0.92rem; color: #475569; line-height: 1.55;">
            Translates the Devanagari output into natural, grammatically sound English with high semantic accuracy and preservation of colloquial tone.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Clean Architectural Pipeline
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Sequential Processing Pipeline</div>", unsafe_allow_html=True)
st.markdown("""
```mermaid
flowchart LR
    A[Roman Hinglish Input] --> B[AI4Bharat IndicXlit]
    B --> C[Devanagari Hindi]
    C --> D[BharatGen Param-1]
    D --> E[Enhanced Hindi]
    E --> F[AI4Bharat IndicTrans2]
    F --> G[English Translation]
```
""", unsafe_allow_html=True)

st.markdown("---")

# Hardware & Foundation Model Inventory
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Model Inventory & Compute Safeguards</div>", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown("**AI4Bharat IndicXlit**")
    st.caption("Primary Transliteration Model")
    st.code(f"ID: {INDICXLIT_MODEL_ID}\nArchitecture: Seq2Seq / G2P Phonetic\nTarget: Roman to Devanagari\nMemory: ~120 MB RAM")

with col_m2:
    st.markdown("**BharatGen Param-1**")
    st.caption("Generative Writing Enhancement")
    st.code(f"ID: {PARAM1_MODEL_ID}\nArchitecture: 2.9B Causal Transformer\nTarget: hin_Deva -> hin_Deva\nExecution: 4-bit / CPU Offload")

with col_m3:
    st.markdown("**AI4Bharat IndicTrans2**")
    st.caption("Primary Machine Translation Model")
    st.code(f"ID: {INDICTRANS2_MODEL_ID}\nArchitecture: Distilled 200M Transformer\nTarget: hin_Deva -> eng_Latn\nFootprint: <0.8 GB VRAM")

# Hardware Telemetry Strip
gpu_info = get_gpu_memory_info()
if gpu_info.get("available"):
    gpu_badge = f"<span class='badge-green'>GPU: {gpu_info.get('name')}</span> <span class='badge-white'>Total VRAM: {gpu_info.get('total_gb')} GB</span> <span class='badge-blue'>Free VRAM: {gpu_info.get('free_gb')} GB</span>"
else:
    gpu_badge = "<span class='badge-white'>Compute: CPU Execution Mode (Safe Fallback)</span>"

st.markdown(f"""
<div style="margin-top: 1.5rem; padding: 0.9rem 1.2rem; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);">
    <span style="font-size: 0.82rem; color: #64748b; font-weight: 500;">Hardware Telemetry:</span>
    <div style="display: flex; gap: 0.5rem; align-items: center;">{gpu_badge}</div>
</div>
""", unsafe_allow_html=True)
