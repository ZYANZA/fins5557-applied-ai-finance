# FINS5557 Applied AI in Finance — Student Notebooks

**UNSW Business School | Postgraduate Course**
**Authors:** Juraj Hric

---

## About This Course

FINS5557 explores how artificial intelligence is transforming the global financial sector. The course equips students with both the conceptual understanding and practical skills needed to work at the intersection of AI and finance.

Topics span AI in banking automation, predictive analytics, risk management, fraud detection, algorithmic trading, and asset and wealth management. The first five weeks build technical foundations; weeks 7–10 focus on industry applications through real-world case studies.

**Format:** 10-week postgraduate course — three-hour weekly lecture (three one-hour sessions per week).

---

## How to Use These Notebooks

All notebooks are designed to run in **Google Colab** with no local setup required.

### Opening a notebook in Colab

1. Navigate to the week folder below.
2. Click the notebook file (`.ipynb`).
3. On GitHub, click **Open in Colab** (the badge at the top of the notebook), or go to [colab.research.google.com](https://colab.research.google.com) → File → Open notebook → GitHub tab → paste this repository URL.

### API keys (weeks with live AI features)

Some notebooks can connect to the Gemini API for live demonstrations. A free key is sufficient:

1. Get a free API key at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no credit card required; free tier provides 15 RPM / 1 million tokens per day.
2. In Colab: click the **key icon** (Secrets panel, left sidebar) → **+ Add new secret** → Name: `GOOGLE_API_KEY`, Value: paste your key, toggle **Notebook access** ON.
3. Re-run the setup cell — the notebook auto-detects the secret.

If no key is provided, every notebook falls back automatically to a **mock simulation** that produces representative output so the full pipeline can still be followed.

### Python stack

Notebooks use the standard course stack — all pre-installed in Colab:

```
numpy  pandas  scipy  scikit-learn  matplotlib  google-generativeai
```

---

## Weekly Notebooks

### Week 01 — AI and Data Literacy for Finance and Banking

| Notebook | Description |
|---|---|
| [week1-seminar.ipynb](week01/week1-seminar.ipynb) | Core seminar: AI methodologies in finance; credit scoring and customer segmentation; data pipeline from raw financial data to model inputs |

**Key concepts:** ML taxonomy, supervised/unsupervised learning, data quality, Digital Data Factory (DDF) pipeline, credit risk scoring.

---

### Week 02 — Applications, Opportunities and Limitations of AI

| Notebook | Description |
|---|---|
| [week2-seminar.ipynb](week02/week2-seminar.ipynb) | Core seminar: AI across the financial services value chain; limitations — hallucination, explainability gaps, model drift |

**Key concepts:** Decision support systems, personalisation engines, real-time anomaly detection, AI regulation, responsible AI.

---

### Week 03 — Advanced Techniques in LLM and Multimodal Models

| Notebook | Description |
|---|---|
| [week3-seminar.ipynb](week03/week3-seminar.ipynb) | Core seminar: Transformer architecture, fine-tuning (LoRA, RAG), multimodal models for earnings calls and document processing |

**Key concepts:** Attention mechanism, tokenisation, BloombergGPT, LoRA fine-tuning, retrieval-augmented generation (RAG), multimodal AI.

---

### Week 04 — AI Virtual Agents, AI Ethics and Use Cases

| Notebook | Description |
|---|---|
| [week4-seminar.ipynb](week04/week4-seminar.ipynb) | Core seminar: Agentic AI systems in finance; AI ethics — fairness, transparency, accountability; hands-on agent design for financial report summarisation |

**Key concepts:** Agentic pipelines, tool use, multi-step reasoning, AI ethics, bias in financial AI, portfolio rebalancing agents.

---

### Week 05 — Banking Transformation

| Notebook | Description |
|---|---|
| [week5-seminar.ipynb](week05/week5-seminar.ipynb) | Core seminar: Digital transformation of banking and insurance; straight-through processing; AI-assisted underwriting; full digitisation case study |

**Key concepts:** Straight-through processing, intelligent document handling, AI underwriting, legacy migration, cloud adoption, model risk.

---

### Week 06 — Tech Lab

| Notebook | Description |
|---|---|
| [week6-seminar.ipynb](week06/week6-seminar.ipynb) | Hands-on lab: Python AI stack for finance — credit risk classifier, earnings report parsing with LLMs, backtesting loop; coding challenges |

**Key concepts:** `pandas`, `scikit-learn`, LLM APIs (Gemini), backtesting, financial data wrangling. *This week is code-first and lighter on prose.*

---

### Week 07 — AI in Corporate Finance

| Notebook | Description |
|---|---|
| [week7-seminar.ipynb](week07/week7-seminar.ipynb) | Core seminar: AI-augmented valuation (DCF, comparable company analysis); NLP on financial filings; FP&A automation; board reporting |

**Key concepts:** Sentiment extraction from filings, ML-based comps, treasury cash forecasting, FP&A automation, CFO digital mandate.

---

### Week 08 — Trading and Investing with AI

| Notebook | Description |
|---|---|
| [week8-case-study.ipynb](week08/week8-case-study.ipynb) | Case study: Algorithmic trading platform vs. long-term AI investment platform — design, governance, and bias analysis |

**Key concepts:** Algorithmic bias, mean-variance optimisation, RL-based allocation, factor models, high-frequency vs. long-horizon strategies.

---

### Week 09 — AI Asset and Wealth Management

| Notebook | Description |
|---|---|
| [week9-case-study.ipynb](week09/week9-case-study.ipynb) | Case study: End-to-end WealthTech platform simulation — client profiling, goals-based planning, portfolio construction, LLM-assisted SOA generation, BID compliance gate |

**Key concepts:** Robo-advisory, goals-based investing, best-interest duty (BID), superannuation AI, WealthTech architecture.

---

### Week 10 — Financial Intelligence

| Notebook | Description |
|---|---|
| [week10-case-study.ipynb](week10/week10-case-study.ipynb) | Case study: ESG compliance, financial inclusion via alternative credit scoring, alternative data (satellite, geospatial), AI-enabled fraud detection |

**Key concepts:** Financial inclusion, alternative data, ESG scoring with FinBERT, greenwashing detection, deepfake fraud, UN SDGs.

---

## Course Structure at a Glance

| Week | Topic | Type |
|------|-------|------|
| 1 | AI and Data Literacy for Finance and Banking | Foundations |
| 2 | Applications, Opportunities and Limitations of AI | Foundations |
| 3 | Advanced Techniques in LLM and Multimodal Models | Technical depth |
| 4 | AI Virtual Agents, AI Ethics and Use Cases | Technical depth |
| 5 | Banking Transformation | Technical depth |
| 6 | Tech Lab | Practical / code |
| 7 | AI in Corporate Finance | Industry application |
| 8 | Trading and Investing with AI | Industry application |
| 9 | AI Asset and Wealth Management | Industry application |
| 10 | Financial Intelligence | Industry application |

---

## Reference Textbooks

* Hilpisch Y., (2021). *Artificial Intelligence in Finance: a Python-based Guide*. O'Reilly
* Alammar Y., Grootendorst M., (2025). *Hands-On Large Language Models: Language Understanding and Generation*, O'Reilly
* Hric, J. & Lin, Y. (2026). *Applied Data Science in FinTech: Models, Tools, and Case Studies*. Routledge.

---

## Licence and Attribution

These materials are provided for enrolled FINS5557 students at UNSW Business School. All notebooks are for educational use only. Please do not redistribute without permission from the course authors.

For questions, contact the course team via the UNSW Moodle page.
