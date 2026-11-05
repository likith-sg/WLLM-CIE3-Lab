"""
About Project - Architecture, Technical Specifications, and Academic Documentation (Light Theme).
Palette: Crisp White, Deep Black, Electric Blue, Mint Light Green.
CS3235 CIE3 Mini Project - AI4Bharat + BharatGen
"""

import streamlit as st
from utils.ui_utils import inject_consumer_css, render_top_navbar

# Page Configuration - Sidebar hidden via CSS
st.set_page_config(
    page_title="About Project | Hinglish AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_consumer_css()
render_top_navbar("about")

# Header
st.markdown('<div class="badge-green" style="display: inline-block; margin-bottom: 0.6rem;">System Documentation</div>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 2.2rem; font-weight: 700; letter-spacing: -0.03em; color: #0f172a; margin-bottom: 0.35rem;">System Architecture & Documentation</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1rem; color: #475569; margin-bottom: 1.5rem;">Technical documentation and architectural specifications for the Hinglish Smart Writing Assistant.</p>', unsafe_allow_html=True)

st.markdown("---")

# Problem Statement & Relevance
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Problem Statement and Motivation</div>", unsafe_allow_html=True)
st.markdown("""
Over 500 million Indian citizens converse in Hindi daily. However, fewer than 10% utilize native Devanagari virtual keyboards due to high cognitive friction and the physical constraints of standard English QWERTY layouts. Consequently, colloquial **Roman-script Hinglish** has become the dominant medium of daily digital messaging, mobile social interactions, and academic communication.

Despite its popularity, Roman Hinglish lacks standardized orthography. A single native word such as **नमस्ते** or **बहुत** is typed inconsistently across users as `namaste / namasthe` or `bohot / bahut / bhut`. Furthermore, colloquial texting frequently contains grammatical agreement errors and informal phrasing unsuitable for academic, administrative, or professional correspondence.

**Hinglish AI** addresses this linguistic challenge by constructing an end-to-end multi-stage neural pipeline that converts phonetic Roman Hinglish into native Devanagari script, applies generative AI styling to rectify grammar and syntax, and translates the refined message into natural English.
""")

st.markdown("---")

# Architectural Diagram
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>System Architecture</div>", unsafe_allow_html=True)

st.markdown("""
```mermaid
flowchart TD
    A[Roman Hinglish Input] --> B[AI4Bharat IndicXlit Engine]
    B --> C[Devanagari Hindi Text]
    C --> D[BharatGen Param-1 Enhancer]
    D --> E[Polished Hindi Text]
    E --> F[AI4Bharat IndicTrans2 Model]
    F --> G[English Translation Output]
```
""")

st.markdown("---")

# Hardware & VRAM Management
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Hardware Performance and VRAM Safeguards</div>", unsafe_allow_html=True)
st.markdown("""
The target system is an **NVIDIA GeForce RTX 3050 Laptop GPU with 4 GB VRAM**. Managing multiple modern deep learning checkpoints within 4 GB VRAM presents significant memory challenges:

1. **Sequential Model Loading & Lazy Initialization:** Neural models are initialized on-demand only when their corresponding actions are triggered.
2. **Precision Optimization:** Models use `torch.float16` on GPU or `torch.float32` CPU fallback to avoid CUDA Out of Memory (OOM) exceptions.
3. **Param-1 Offload Strategy:** For the 2.9B parameter BharatGen foundation model (~5.8 GB in fp16), the architecture includes CPU offloading and modular hybrid execution.
4. **VRAM Safety Guards:** The system queries available GPU VRAM before allocating model tensors and falls back to CPU if free VRAM is below 800 MB.
""")

st.markdown("---")

# Evaluation Methodology
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Quantitative Evaluation Methodology</div>", unsafe_allow_html=True)
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
st.markdown("<div style='font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 0.8rem;'>Official Resources and Citations</div>", unsafe_allow_html=True)
st.markdown("""
- **AI4Bharat IndicXlit:** [https://github.com/AI4Bharat/IndicXlit](https://github.com/AI4Bharat/IndicXlit)
- **AI4Bharat IndicTrans2:** [https://github.com/AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2)
- **BharatGen AI Organization:** [https://huggingface.co/bharatgenai](https://huggingface.co/bharatgenai)
- **Aksharantar Benchmark Dataset:** [https://github.com/AI4Bharat/IndianNLP-Transliteration](https://github.com/AI4Bharat/IndianNLP-Transliteration)
""")
