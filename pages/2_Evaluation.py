"""
Evaluation Dashboard - Quantitative Benchmark & Error Taxonomy.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import json
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st

from utils.ui_utils import inject_consumer_css
from evaluation.evaluate import run_full_evaluation, RESULTS_FILE, DATASET_FILE

st.set_page_config(
    page_title="Evaluation Dashboard | HINGLISH AI",
    page_icon="📊",
    layout="wide"
)

inject_consumer_css()

st.markdown('<div class="hero-badge">Quantitative Research Assessment</div>', unsafe_allow_html=True)
st.markdown('<h2 style="font-weight: 800; margin-bottom: 0.2rem;">Quantitative Evaluation & Diagnostics</h2>', unsafe_allow_html=True)
st.caption("Empirical performance evaluation across 40 test cases from the Aksharantar benchmark spanning 10 linguistic categories.")

st.markdown("---")

# Re-run benchmark action
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.write("Real-time pipeline evaluation against ground-truth references verified for CS3235 assessment.")
with col_top2:
    if st.button("🔄 Re-run 40-Sample Benchmark", type="primary", use_container_width=True):
        with st.spinner("Executing live evaluation on test cases..."):
            results = run_full_evaluation()
            st.success("Evaluation complete! Dashboard refreshed.")
            st.rerun()

# Load latest evaluation data
if not RESULTS_FILE.exists():
    with st.spinner("Initializing evaluation results..."):
        results = run_full_evaluation()
else:
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

# High-Level Metric Tiles
m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{results['total_test_cases']}</div>
        <div class="metric-label">Total Test Cases</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value" style="color:#4F46E5;">{results['average_cer'] * 100:.1f}%</div>
        <div class="metric-label">Average CER</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value" style="color:#059669;">{results['average_word_accuracy']:.1f}%</div>
        <div class="metric-label">Word Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value" style="color:#2563EB;">{results['corpus_cer'] * 100:.1f}%</div>
        <div class="metric-label">Corpus CER</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value" style="color:#7C3AED;">{results['average_bleu']:.1f}</div>
        <div class="metric-label">Average BLEU</div>
    </div>
    """, unsafe_allow_html=True)

with m6:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value" style="color:#D97706;">{results['average_chrf']:.1f}</div>
        <div class="metric-label">Average chrF</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Visual Charts
st.markdown("### 📈 Category Performance Analysis")

category_df = pd.DataFrame(results["category_breakdown"])

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("##### Word Accuracy by Category (%)")
    chart_acc = alt.Chart(category_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X("avg_word_accuracy:Q", title="Word Accuracy (%)", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("category:N", sort="-x", title="Linguistic Category"),
        color=alt.Color("avg_word_accuracy:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=["category", "test_cases", "avg_word_accuracy", "perfect_matches"]
    ).properties(height=320)
    st.altair_chart(chart_acc, use_container_width=True)

with col_chart2:
    st.markdown("##### Character Error Rate by Category (Lower is Better)")
    chart_cer = alt.Chart(category_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X("avg_cer:Q", title="Character Error Rate (CER)", scale=alt.Scale(domain=[0, 0.4])),
        y=alt.Y("category:N", sort="x", title="Linguistic Category"),
        color=alt.Color("avg_cer:Q", scale=alt.Scale(scheme="purples", reverse=True), legend=None),
        tooltip=["category", "test_cases", "avg_cer", "avg_bleu"]
    ).properties(height=320)
    st.altair_chart(chart_cer, use_container_width=True)

st.markdown("---")

# Failure Taxonomy Breakdown
st.markdown("### 🔬 Failure Analysis & Diagnostic Taxonomy")
failure_data = results.get("failure_analysis", {})
category_breakdown = failure_data.get("category_breakdown", {})

fail_cols = st.columns(4)
idx = 0
for cat_key, count in category_breakdown.items():
    if count > 0:
        with fail_cols[idx % 4]:
            st.metric(label=cat_key.replace("_", " ").title(), value=f"{count} cases")
        idx += 1

st.markdown("#### Diagnostic Case Studies")
sample_failures = failure_data.get("sample_failure_cases", [])
if sample_failures:
    for case in sample_failures[:4]:
        with st.expander(f"Case {case['id']}: [{case['category']}] - '{case['input']}'"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown(f"**Expected Hindi:** `{case['expected']}`")
                st.markdown(f"**Actual Output:** `{case['predicted']}`")
            with c_f2:
                st.markdown(f"**Explanation:** {case['explanation']}")
                st.markdown(f"**Remediation:** {case['suggestion']}")
else:
    st.info("No failure cases detected in the selected run.")

st.markdown("---")

# Detailed Test Cases Table
st.markdown("### 📋 Complete Benchmark Dataset & Predictions")

details_df = pd.DataFrame(results["detailed_results"])

# Filtering
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    search_q = st.text_input("Search test cases (input, reference, or Hindi text):", "")
with col_f2:
    selected_cat = st.selectbox("Filter by Category:", ["All Categories"] + list(category_df["category"].unique()))

filtered_df = details_df.copy()
if selected_cat != "All Categories":
    filtered_df = filtered_df[filtered_df["category"] == selected_cat]

if search_q.strip():
    q = search_q.lower()
    filtered_df = filtered_df[
        filtered_df["input_hinglish"].str.lower().str.contains(q) |
        filtered_df["reference_hindi"].str.contains(q) |
        filtered_df["predicted_hindi"].str.contains(q)
    ]

# Display table
st.dataframe(
    filtered_df[[
        "id", "category", "input_hinglish", "reference_hindi",
        "predicted_hindi", "cer", "word_accuracy", "reference_english", "predicted_english", "bleu"
    ]],
    use_container_width=True,
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

# Export Data Section
st.download_button(
    label="📥 Download Full Evaluation JSON",
    data=json.dumps(results, ensure_ascii=False, indent=2),
    file_name="hinglish_ai_evaluation_results.json",
    mime="application/json"
)
