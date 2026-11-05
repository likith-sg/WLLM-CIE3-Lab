"""
Evaluation Dashboard - Quantitative Benchmark and Diagnostic Error Taxonomy.
Solid Apple Light Theme with Native Container Cards (Zero Code Leaks, Zero Text Collisions).
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import json
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st

from utils.ui_utils import inject_consumer_css, render_top_navbar
from evaluation.evaluate import run_full_evaluation, RESULTS_FILE, DATASET_FILE

# Page Configuration - Sidebar hidden via CSS
st.set_page_config(
    page_title="Evaluation Dashboard | Hinglish AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_consumer_css()
render_top_navbar("evaluation")

# Load evaluation data
if not RESULTS_FILE.exists():
    with st.spinner("Initializing evaluation results..."):
        results = run_full_evaluation()
else:
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

# Header Section
col_head1, col_head2 = st.columns([3, 1.2])
with col_head1:
    st.markdown('<div class="badge-green" style="display: inline-block; margin-bottom: 0.6rem;">Empirical Benchmark</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.3rem; font-weight: 800; letter-spacing: -0.035em; color: #0f172a; margin-bottom: 0.35rem;">Evaluation & Diagnostics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.05rem; color: #475569; margin-bottom: 1.25rem;">Quantitative assessment across 40 curated test cases from the AI4Bharat Aksharantar corpus spanning 10 linguistic domains.</p>', unsafe_allow_html=True)

with col_head2:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    if st.button("Run Live Benchmark", type="primary", use_container_width=True):
        with st.spinner("Executing evaluation across 40 test cases..."):
            results = run_full_evaluation()
            st.toast("Evaluation benchmark refreshed.")
            st.rerun()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# 4 Flagship Hero Metric Cards
c_m1, c_m2, c_m3, c_m4 = st.columns(4)

with c_m1:
    st.markdown(f"""
    <div class="metric-activity-card">
        <div class="metric-activity-value" style="color: #059669;">{results['average_word_accuracy']:.1f}%</div>
        <div class="metric-activity-label">Word Accuracy</div>
        <div class="metric-activity-subtext">Exact word correctness across corpus</div>
    </div>
    """, unsafe_allow_html=True)

with c_m2:
    st.markdown(f"""
    <div class="metric-activity-card">
        <div class="metric-activity-value" style="color: #0071e3;">{results['average_cer'] * 100:.1f}%</div>
        <div class="metric-activity-label">Average CER</div>
        <div class="metric-activity-subtext">Mean character error rate</div>
    </div>
    """, unsafe_allow_html=True)

with c_m3:
    st.markdown(f"""
    <div class="metric-activity-card">
        <div class="metric-activity-value" style="color: #2563eb;">{results['average_bleu']:.1f}</div>
        <div class="metric-activity-label">Translation BLEU</div>
        <div class="metric-activity-subtext">SacreBLEU benchmark score</div>
    </div>
    """, unsafe_allow_html=True)

with c_m4:
    st.markdown(f"""
    <div class="metric-activity-card">
        <div class="metric-activity-value" style="color: #0f172a;">{results['average_chrf']:.1f}</div>
        <div class="metric-activity-label">Translation chrF</div>
        <div class="metric-activity-subtext">Character n-gram F-score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Visual Analytics Section
st.markdown("<div style='font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.9rem;'>Visual Performance Analytics</div>", unsafe_allow_html=True)

category_df = pd.DataFrame(results["category_breakdown"])

tab_chart_acc, tab_chart_cer = st.tabs([
    "Word Accuracy by Linguistic Domain (%)",
    "Character Error Rate (CER) - Lower is Better"
])

with tab_chart_acc:
    st.markdown("<div style='font-size: 0.92rem; font-weight: 700; color: #0f172a; margin-bottom: 12px;'>Word Accuracy Across 10 Linguistic Categories (%)</div>", unsafe_allow_html=True)
    chart_acc = alt.Chart(category_df).mark_bar(
        cornerRadiusTopRight=6, 
        cornerRadiusBottomRight=6, 
        height=24,
        color="#0071e3"
    ).encode(
        x=alt.X("avg_word_accuracy:Q", title="Word Accuracy (%)", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(labelColor="#475569", titleColor="#0f172a")),
        y=alt.Y("category:N", sort="-x", title=None, axis=alt.Axis(labelLimit=300, labelFontSize=12, labelFontWeight="bold", labelColor="#0f172a")),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("test_cases:Q", title="Test Cases"),
            alt.Tooltip("avg_word_accuracy:Q", title="Word Accuracy (%)", format=".1f"),
            alt.Tooltip("perfect_matches:Q", title="Perfect Matches")
        ]
    ).properties(height=360)
    st.altair_chart(chart_acc, use_container_width=True)

with tab_chart_cer:
    st.markdown("<div style='font-size: 0.92rem; font-weight: 700; color: #0f172a; margin-bottom: 12px;'>Character Error Rate (CER) Across 10 Categories (Lower is Better)</div>", unsafe_allow_html=True)
    chart_cer = alt.Chart(category_df).mark_bar(
        cornerRadiusTopRight=6, 
        cornerRadiusBottomRight=6, 
        height=24,
        color="#059669"
    ).encode(
        x=alt.X("avg_cer:Q", title="Character Error Rate (CER)", scale=alt.Scale(domain=[0, 0.35]), axis=alt.Axis(labelColor="#475569", titleColor="#0f172a", format="%")),
        y=alt.Y("category:N", sort="x", title=None, axis=alt.Axis(labelLimit=300, labelFontSize=12, labelFontWeight="bold", labelColor="#0f172a")),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("test_cases:Q", title="Test Cases"),
            alt.Tooltip("avg_cer:Q", title="Avg CER", format=".3f"),
            alt.Tooltip("avg_bleu:Q", title="Avg BLEU", format=".1f")
        ]
    ).properties(height=360)
    st.altair_chart(chart_cer, use_container_width=True)

st.markdown("---")

# Failure Taxonomy Section
st.markdown("<div style='font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.9rem;'>Failure Analysis & Diagnostic Taxonomy</div>", unsafe_allow_html=True)
failure_data = results.get("failure_analysis", {})
category_breakdown = failure_data.get("category_breakdown", {})

active_failures = [(k, v) for k, v in category_breakdown.items() if v > 0]
if active_failures:
    fail_cols = st.columns(min(len(active_failures), 4))
    for i, (cat_key, count) in enumerate(active_failures[:4]):
        with fail_cols[i]:
            st.markdown(f"""
            <div class="metric-activity-card" style="text-align: center; padding: 1.1rem;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #0071e3; line-height: 1;">{count}</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #334155; text-transform: uppercase; margin-top: 6px;">{cat_key.replace('_', ' ')}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 8px;'>Diagnostic Case Studies</div>", unsafe_allow_html=True)

sample_failures = failure_data.get("sample_failure_cases", [])
if sample_failures:
    for case in sample_failures[:4]:
        with st.expander(f"Case {case['id']}: {case['category']} - '{case['input']}'"):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(f"**Expected Hindi:** `{case['expected']}`")
                st.markdown(f"**Model Output:** `{case['predicted']}`")
            with col_d2:
                st.markdown(f"**Root Cause:** {case['explanation']}")
                st.markdown(f"**Remediation:** {case['suggestion']}")
else:
    st.info("No failure cases detected in the selected run.")

st.markdown("---")

# Benchmark Test Case Inspector (Rendered with Native Streamlit Containers - ZERO Code Leaks)
st.markdown("<div style='font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.9rem;'>Benchmark Test Case Inspector</div>", unsafe_allow_html=True)

details_df = pd.DataFrame(results["detailed_results"])

# Filter Controls
f_col1, f_col2, f_col3 = st.columns([2.5, 1.5, 1.2])

with f_col1:
    search_query = st.text_input(
        "Search Test Cases", 
        value="", 
        placeholder="Search by Roman input, Hindi, or English text...",
        label_visibility="collapsed"
    )

with f_col2:
    all_cats = ["All Categories"] + list(category_df["category"].unique())
    selected_category = st.selectbox(
        "Filter Category", 
        options=all_cats,
        label_visibility="collapsed"
    )

with f_col3:
    match_filter = st.selectbox(
        "Match Quality", 
        options=["All Matches", "Perfect (CER = 0%)", "High Quality (<15%)", "Discrepancy (>=15%)"],
        label_visibility="collapsed"
    )

# Filter Data
filtered_cases = details_df.copy()

if selected_category != "All Categories":
    filtered_cases = filtered_cases[filtered_cases["category"] == selected_category]

if match_filter == "Perfect (CER = 0%)":
    filtered_cases = filtered_cases[filtered_cases["cer"] == 0.0]
elif match_filter == "High Quality (<15%)":
    filtered_cases = filtered_cases[(filtered_cases["cer"] > 0.0) & (filtered_cases["cer"] < 0.15)]
elif match_filter == "Discrepancy (>=15%)":
    filtered_cases = filtered_cases[filtered_cases["cer"] >= 0.15]

if search_query.strip():
    q = search_query.lower()
    filtered_cases = filtered_cases[
        filtered_cases["input_hinglish"].str.lower().str.contains(q) |
        filtered_cases["reference_hindi"].str.contains(q) |
        filtered_cases["predicted_hindi"].str.contains(q) |
        filtered_cases["reference_english"].str.lower().str.contains(q)
    ]

# View Mode Switch
tab_cards, tab_table = st.tabs(["Interactive Case Cards (Recommended)", "Tabular Data Grid"])

with tab_cards:
    total_found = len(filtered_cases)
    
    col_count, col_page_size = st.columns([3, 1])
    with col_count:
        st.markdown(f"<div style='font-size: 0.84rem; color: #64748b; padding-top: 6px;'>Showing <strong>{total_found}</strong> matching test cases:</div>", unsafe_allow_html=True)
    with col_page_size:
        max_display = st.selectbox("Display Count:", [10, 20, "All 40"], index=0, label_visibility="collapsed")
    
    if max_display == "All 40":
        cases_to_show = filtered_cases
    else:
        cases_to_show = filtered_cases.head(int(max_display))

    if total_found == 0:
        st.info("No test cases match the active filter criteria.")
    else:
        # Render clean cards using native Streamlit containers
        for _, row in cases_to_show.iterrows():
            cer_val = row["cer"]
            if cer_val == 0.0:
                badge_html = '<span class="badge-green">Perfect Match (CER: 0.0%)</span>'
            elif cer_val < 0.15:
                badge_html = f'<span class="badge-blue">High Fidelity (CER: {cer_val*100:.1f}%)</span>'
            else:
                badge_html = f'<span class="badge-amber">Discrepancy (CER: {cer_val*100:.1f}%)</span>'

            with st.container(border=True):
                # Header row
                c_top1, c_top2 = st.columns([3, 1.5])
                with c_top1:
                    st.markdown(f"**Case #{row['id']}** &nbsp; <span class='badge-slate'>{row['category']}</span>", unsafe_allow_html=True)
                with c_top2:
                    st.markdown(f"<div style='text-align: right;'>{badge_html}</div>", unsafe_allow_html=True)

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

                # Source Input
                st.caption("SOURCE ROMAN HINGLISH")
                st.markdown(f"<div style='font-size: 1.15rem; font-weight: 600; color: #0071e3;'>{row['input_hinglish']}</div>", unsafe_allow_html=True)

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                # Side-by-side Hindi & English comparison
                col_h, col_e = st.columns(2)
                with col_h:
                    st.caption("DEVANAGARI HINDI TRANSLITERATION")
                    st.markdown(f"**Predicted:** {row['predicted_hindi']}")
                    st.markdown(f"<span style='color: #64748b;'>Reference: {row['reference_hindi']}</span>", unsafe_allow_html=True)

                with col_e:
                    st.caption("ENGLISH TRANSLATION")
                    st.markdown(f"**Predicted:** {row['predicted_english']}")
                    st.markdown(f"<span style='color: #64748b;'>Reference: {row['reference_english']}</span>", unsafe_allow_html=True)

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                
                # Bottom metric badges
                st.markdown(f"""
                <div style='font-size: 0.76rem; color: #64748b; padding-top: 8px; border-top: 1px solid #f1f5f9;'>
                    <strong>Metrics:</strong> CER: <strong>{row['cer']*100:.1f}%</strong> &bull; Word Accuracy: <strong>{row['word_accuracy']:.1f}%</strong> &bull; BLEU: <strong>{row['bleu']:.1f}</strong>
                </div>
                """, unsafe_allow_html=True)

with tab_table:
    st.dataframe(
        filtered_cases[[
            "id", "category", "input_hinglish", "reference_hindi",
            "predicted_hindi", "cer", "word_accuracy", "reference_english", "predicted_english", "bleu"
        ]],
        use_container_width=True,
        height=400,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "category": st.column_config.TextColumn("Category", width="medium"),
            "input_hinglish": st.column_config.TextColumn("Roman Input", width="large"),
            "reference_hindi": st.column_config.TextColumn("Reference Hindi", width="large"),
            "predicted_hindi": st.column_config.TextColumn("Predicted Hindi", width="large"),
            "cer": st.column_config.NumberColumn("CER", format="%.3f"),
            "word_accuracy": st.column_config.NumberColumn("Word Acc %", format="%.1f%%"),
            "reference_english": st.column_config.TextColumn("Ref English", width="large"),
            "predicted_english": st.column_config.TextColumn("Predicted English", width="large"),
            "bleu": st.column_config.NumberColumn("BLEU", format="%.1f")
        },
        hide_index=True
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Export Data Action
col_exp1, col_exp2 = st.columns([1.5, 3])
with col_exp1:
    st.download_button(
        label="Export Full Benchmark JSON",
        data=json.dumps(results, ensure_ascii=False, indent=2),
        file_name="hinglish_ai_benchmark_results.json",
        mime="application/json",
        use_container_width=True
    )
