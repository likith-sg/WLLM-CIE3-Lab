"""
Apple Light Design System (Zero Gradients, Clean Solid Modern Palette).
Colors: White (#ffffff), Light Background (#f8fafc), Solid Apple Blue (#0071e3),
Mint Green (#059669), and Slate Black (#0f172a).
"""

import streamlit as st

APPLE_SOLID_LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* CSS Reset & Global Layout */
    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Completely eliminate Streamlit sidebar and collapse buttons */
    [data-testid="stSidebar"], 
    section[data-testid="stSidebar"], 
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Streamlit Main Container Optimization */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1220px !important;
        margin: 0 auto !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        display: none !important;
    }

    /* Target standard typography without breaking Streamlit icon fonts/ligatures */
    html, body, p, h1, h2, h3, h4, h5, h6, input, textarea, select {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Inter", sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        letter-spacing: -0.012em;
        color: #0f172a;
    }

    /* Apple Top Navigation Bar - Solid White & Clean Border */
    .apple-top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.85rem 1.4rem;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }

    .apple-nav-brand {
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }

    .apple-nav-badge-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background-color: #0f172a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.82rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }

    .apple-nav-title {
        font-size: 0.98rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #0f172a;
        margin: 0;
        line-height: 1.2;
    }

    .apple-nav-desc {
        font-size: 0.74rem;
        color: #64748b;
        margin-top: 1px;
    }

    /* Top Page Navigation Pills */
    div[data-testid="stPageLink"] a {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #334155 !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.15s ease !important;
        text-decoration: none !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stPageLink"] a:hover {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0071e3 !important;
    }

    div[data-testid="stPageLink"] a[aria-current="page"] {
        background-color: #0071e3 !important;
        border-color: #0071e3 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0, 113, 227, 0.25) !important;
    }

    /* Apple Pro Workspace Cards */
    .apple-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
    }

    .apple-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.85rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f1f5f9;
    }

    .apple-card-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0f172a;
    }

    /* Badges - Solid Colors Only (No Gradients) */
    .badge-blue {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        background-color: #eff6ff;
        color: #0071e3;
        border: 1px solid #bfdbfe;
    }

    .badge-green {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        background-color: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
    }

    .badge-slate {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }

    .badge-amber {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        background-color: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }

    /* Output Displays */
    .output-display-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
    }

    .output-devanagari-hero {
        font-family: 'Noto Sans Devanagari', sans-serif !important;
        font-size: 1.55rem;
        line-height: 1.65;
        font-weight: 600;
        color: #0f172a;
        min-height: 68px;
        word-break: break-word;
        padding-top: 4px;
    }

    .output-english-hero {
        font-size: 1.35rem;
        line-height: 1.55;
        font-weight: 500;
        color: #1e293b;
        min-height: 60px;
        word-break: break-word;
        letter-spacing: -0.015em;
        padding-top: 4px;
    }

    /* Comparison Cards */
    .matrix-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.15rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .matrix-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.65rem;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.4rem;
    }

    .matrix-title {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }

    .matrix-content {
        font-size: 1.08rem;
        line-height: 1.5;
        color: #0f172a;
        min-height: 50px;
        word-break: break-word;
        font-weight: 500;
    }

    .matrix-content-devanagari {
        font-family: 'Noto Sans Devanagari', sans-serif !important;
        font-size: 1.22rem;
        font-weight: 600;
        color: #0f172a;
    }

    /* Metric Activity Tiles - Solid White with Clean Borders */
    .metric-activity-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .metric-activity-value {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .metric-activity-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #0f172a;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .metric-activity-subtext {
        font-size: 0.73rem;
        color: #64748b;
        margin-top: 3px;
    }

    /* Streamlit Container Border Styling (Native Card) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 0.85rem !important;
    }

    /* Streamlit Expander - Clean Light Theme */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin-bottom: 0.65rem !important;
        overflow: hidden !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    [data-testid="stExpander"] details {
        border: none !important;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #0f172a !important;
        padding: 0.75rem 1rem !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: #f8fafc !important;
    }

    /* Streamlit Text Area Override */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 1.15rem !important;
        line-height: 1.65 !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 0.95rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    .stTextArea textarea:focus {
        border-color: #0071e3 !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15) !important;
    }

    /* Streamlit Primary Button - Solid Apple Blue */
    div.stButton > button[kind="primary"] {
        background-color: #0071e3 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.3rem !important;
        box-shadow: 0 2px 6px rgba(0, 113, 227, 0.25) !important;
        transition: all 0.15s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #0077ed !important;
        box-shadow: 0 4px 10px rgba(0, 113, 227, 0.35) !important;
    }

    /* Streamlit Secondary Button - Solid White with Border */
    div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 0.55rem 1rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.15s ease !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background-color: #f8fafc !important;
        border-color: #94a3b8 !important;
        color: #0071e3 !important;
    }

    /* Streamlit Tabs - Apple Segmented Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3px !important;
        background-color: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        width: 100% !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 36px !important;
        border-radius: 7px !important;
        color: #64748b !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0 14px !important;
        background-color: transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }

    /* Selectbox Override */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }

    /* Dividers */
    hr {
        border-color: #e2e8f0 !important;
        margin: 1.5rem 0 !important;
    }
</style>
"""

def inject_consumer_css():
    """Injects solid Apple Light aesthetic into Streamlit."""
    st.markdown(APPLE_SOLID_LIGHT_CSS, unsafe_allow_html=True)

def render_top_navbar(current_page: str = "studio"):
    """
    Renders clean top navigation bar.
    """
    st.markdown("""
    <div class="apple-top-nav">
        <div class="apple-nav-brand">
            <div class="apple-nav-badge-icon">HA</div>
            <div>
                <div class="apple-nav-title">Hinglish Writing Assistant</div>
                <div class="apple-nav-desc">AI4Bharat IndicXlit & IndicTrans2 · BharatGen Param-1</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean top navigation pills
    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
    with nav_col1:
        st.page_link("pages/1_Writing_Assistant.py", label="Writing Studio")
    with nav_col2:
        st.page_link("pages/2_Evaluation.py", label="Benchmark & Metrics")
    with nav_col3:
        st.page_link("pages/3_About.py", label="System Architecture")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
