"""
About Project - Architecture, Technical Specifications, and Academic Documentation.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import streamlit as st
from utils.ui_utils import inject_consumer_css

st.set_page_config(
    page_title="About Project | HINGLISH AI",
    page_icon="📖",
    layout="wide"
)

inject_consumer_css()

st.markdown('<div class="hero-badge">CS3235 CIE3 Mini Project</div>', unsafe_allow_html=True)
st.markdown('<h2 style="font-weight: 800; margin-bottom: 0.2rem;">Project Documentation & System Architecture</h2>', unsafe_allow_html=True)
st.caption("Technical documentation for the Hinglish Smart Writing Assistant individual undergraduate LLM project.")

st.markdown("---")

# Academic Metadata Card
col_meta1, col_meta2 = st.columns(2)
with col_meta1:
    st.markdown("""
    **Course:** CS3235 - Natural Language Processing & Large Language Models  
    **Assessment:** CIE3 Lab Mini Project  
    **Submission Type:** Individual Project  
    **Date:** November 2026  
    """)

with col_meta2:
    st.markdown("""
    **Student Developer:** Likith S G  
    **Target Hardware:** Windows 11 Laptop, NVIDIA RTX 3050 (4 GB VRAM)  
    **Core Technologies:** AI4Bharat IndicXlit, IndicTrans2, BharatGen Param-1, Aksharantar  
    """)

st.markdown("---")

# Problem Statement & Motivation
st.markdown("### 📌 Problem Statement & Relevance")
st.markdown("""
Over 500 million Indian citizens converse in Hindi, yet fewer than 10% utilize native Devanagari virtual keyboards due to high cognitive friction and the physical constraints of standard English QWERTY layouts. Consequently, colloquial **Roman-script Hinglish** has become the dominant medium of daily digital messaging, mobile social interactions, and student discussions.

However, Roman Hinglish lacks standardized orthography. A single native word such as **नमस्ते** or **बहुत** is typed inconsistently across users as `namaste / namasthe` or `bohot / bahut / bhut`. Furthermore, colloquial texting frequently contains grammatical agreement errors and informal phrasing unsuitable for academic, administrative, or professional correspondence.

**Hinglish AI** solves this linguistic chasm by constructing an end-to-end multi-stage pipeline that converts phonetic Roman Hinglish into native Devanagari script, applies generative AI styling to rectify grammar and syntax, and translates the refined message into natural English.
""")

st.markdown("---")

# Architectural Diagram
st.markdown("### 🏗️ System Architecture")
st.markdown("""
```mermaid
graph TD
    A["👤 User Input: Roman Hinglish"] --> B["🔤 IndicXlit Service<br/><i>ai4bharat/indicxlit-en-indic-v1.0</i>"]
    B --> C["📝 Native Devanagari Hindi Text"]
    C --> D["✨ BharatGen Param-1 Service<br/><i>bharatgenai/Param-1-2.9B-Instruct</i>"]
    D --> E["💎 Stylistically Enhanced Hindi"]
    E --> F["🌐 IndicTrans2 Service<br/><i>ai4bharat/indictrans2-indic-en-dist-200M</i>"]
    F --> G["🇬🇧 Idiomatic English Output"]

    subgraph Evaluation Harness
        DS[("Aksharantar Benchmark Dataset<br/>40 Test Cases")] --> Runner["Automated Metric Runner"]
        Runner --> CER["Character Error Rate (CER)"]
        Runner --> WA["Word Accuracy & WER"]
        Runner --> BLEU["BLEU & chrF Translation Quality"]
        Runner --> TAX["8-Category Error Taxonomy"]
    end
```
""")

st.markdown("---")

# Hardware & VRAM Management
st.markdown("### ⚡ Hardware Performance & VRAM Constraints")
st.markdown("""
The target system is an **NVIDIA GeForce RTX 3050 Laptop GPU with 4 GB VRAM**. Managing multiple modern deep learning checkpoints within 4 GB VRAM presents significant memory challenges:

1. **Sequential Model Loading & Lazy Initialization:** Models are loaded on-demand rather than simultaneously hogging VRAM on startup.
2. **Precision Optimization:** Models use `torch.float16` on GPU or `torch.float32` CPU fallback to avoid CUDA Out of Memory (OOM) exceptions.
3. **Param-1 Offload Strategy:** For the 2.9B parameter BharatGen foundation model (~5.8 GB in fp16), the architecture includes CPU offloading and modular hybrid execution.
4. **VRAM Safety Guards:** The system queries available GPU VRAM before allocating model tensors and falls back to CPU if free VRAM is below 800 MB.
""")

st.markdown("---")

# Evaluation Methodology
st.markdown("### 📊 Quantitative Evaluation Methodology")
st.markdown("""
The system is evaluated on **40 representative test cases** derived from AI4Bharat's **Aksharantar benchmark**, spanning 10 communicative categories:
1. Simple words
2. Short sentences
3. Long sentences
4. Questions
5. Commands and requests
6. Conversational Hindi
7. Educational expressions
8. Mixed Hindi-English expressions
9. Ambiguous Roman spellings
10. Punctuation and number patterns

#### Evaluated Metrics:
- **Character Error Rate (CER):** Calculated using Levenshtein distance on normalized Unicode NFC strings:
  $$\\text{CER} = \\frac{S + I + D}{N_{\\text{ref}}}$$
- **Word Accuracy (WA):** Proportion of reference words correctly predicted:
  $$\\text{WA} = \\frac{\\text{Correct Words}}{N_{\\text{ref}}} \\times 100\\%$$
- **Translation Quality:** Evaluated with sentence-level **BLEU** and **chrF** character n-gram F-scores.
""")

st.markdown("---")

# Official References
st.markdown("### 📚 Official Resources & Citations")
st.markdown("""
- **AI4Bharat IndicXlit:** [https://github.com/AI4Bharat/IndicXlit](https://github.com/AI4Bharat/IndicXlit)
- **AI4Bharat IndicTrans2:** [https://github.com/AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2)
- **BharatGen AI Organization:** [https://huggingface.co/bharatgenai](https://huggingface.co/bharatgenai)
- **Aksharantar Benchmark Dataset:** [https://github.com/AI4Bharat/IndianNLP-Transliteration](https://github.com/AI4Bharat/IndianNLP-Transliteration)
""")
