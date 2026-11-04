"""
Modern Consumer-Grade SaaS Design System for Hinglish AI.
Inspired by Linear, DeepL, and Notion AI.
Features theme-adaptive styling, polished glassmorphism, responsive cards,
and sleek typography for Roman and Devanagari text.
"""

import streamlit as st

CONSUMER_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Streamlit Main Container Adjustment */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* Top Brand Navigation Bar */
    .brand-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1.25rem;
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        backdrop-filter: blur(16px);
        margin-bottom: 1.5rem;
    }

    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .brand-logo {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }

    .brand-text-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .brand-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Quick Preset Chips */
    .chips-bar {
        display: flex;
        gap: 0.5rem;
        overflow-x: auto;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Editor Canvas Cards */
    .editor-container {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 18px;
        padding: 1.4rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .editor-container:focus-within {
        border-color: rgba(99, 102, 241, 0.55);
        box-shadow: 0 12px 35px -8px rgba(99, 102, 241, 0.25);
    }

    .editor-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }

    .editor-header-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
    }

    /* Hero Output Display */
    .hero-output-box {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.7));
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.45);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .hero-output-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899);
    }

    .hero-output-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }

    .hero-output-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #C7D2FE;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .hero-devanagari-text {
        font-family: 'Noto Sans Devanagari', sans-serif !important;
        font-size: 1.55rem;
        line-height: 1.65;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: 0.01em;
        min-height: 75px;
    }

    .hero-english-text {
        font-size: 1.35rem;
        line-height: 1.6;
        font-weight: 500;
        color: #F1F5F9;
        min-height: 60px;
    }

    /* Sleek Comparison Cards */
    .compare-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.2rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }

    .compare-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.16);
    }

    .compare-card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }

    .compare-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #94A3B8;
    }

    .compare-body {
        font-size: 1.15rem;
        line-height: 1.55;
        color: #F8FAFC;
        min-height: 55px;
        word-break: break-word;
    }

    .compare-body-hindi {
        font-family: 'Noto Sans Devanagari', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 500;
        color: #FFFFFF;
    }

    /* Pill Badges */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
    }

    .pill-indigo {
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.35);
    }

    .pill-purple {
        background: rgba(168, 85, 247, 0.15);
        color: #D8B4FE;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }

    .pill-emerald {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .pill-slate {
        background: rgba(148, 163, 184, 0.15);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }

    /* Custom Streamlit Buttons override */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.55) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: rgba(30, 41, 59, 0.6) !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: rgba(51, 65, 85, 0.8) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        color: #FFFFFF !important;
    }

    /* Streamlit Textarea styling */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.5) !important;
        color: #F8FAFC !important;
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.9rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
</style>
"""

def inject_consumer_css():
    """Injects high-end consumer UI styles into Streamlit."""
    st.markdown(CONSUMER_CSS, unsafe_allow_html=True)
