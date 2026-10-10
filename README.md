# Applied AI in Finance — FINS3657 / FINS5557 Course Materials

**UNSW Business School — School of Banking and Finance**
**Author:** Juraj Hric

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZYANZA/fins5557-applied-ai-finance)

---

## About This Repository

This repository holds the hands-on teaching materials for two UNSW courses on applied artificial intelligence in finance:

| Course | Level | Audience |
|---|---|---|
| **FINS3657** | Undergraduate | Later-year Bachelor of Commerce and related students |
| **FINS5557** | Postgraduate | Master of Commerce, Master of Finance and related students |

Both courses share one set of weekly seminar notebooks, case studies and lab apps. Lectures, readings, assessment details and due dates differ between the two courses and are published **only on each course's Moodle page**. If this repository and Moodle disagree, follow Moodle.

The courses show how AI is changing the financial sector, covering banking automation, predictive analytics, risk management, fraud detection, algorithmic trading, and asset and wealth management. Weeks 1–5 build the conceptual and technical foundations, Week 6 is a code-first lab, and Weeks 7–10 apply these tools to industry case studies.

**Format:** 10 teaching weeks, with a three-hour weekly lecture (three one-hour sessions).

---

## Repository Layout

```
week01/ … week05/   Seminar notebooks — foundations and technical depth
week06/             Tech Lab — notebook plus Streamlit apps (credit, robo-advice, super fund)
week07/             Seminar notebook — AI in corporate finance
week08/ … week10/   Case-study notebooks — industry applications
week09/             Also contains the WealthTech advisory Streamlit app
```

Each week folder is self-contained. Notebooks generate their own synthetic data or download it at run time, so no separate dataset download is needed.

---

## How to Use These Materials

### Option A — Google Colab (recommended)

All notebooks are designed to run in **Google Colab**, which needs no local setup.

1. Open the week folder you need in this repository and click the `.ipynb` file.
2. Click the **Open in Colab** badge at the top of the notebook. You can also go to [colab.research.google.com](https://colab.research.google.com), choose **File → Open notebook → GitHub**, and paste this repository's URL.
3. Choose **File → Save a copy in Drive** before making changes. Your edits will then be kept in your own Drive.
4. Run the cells from top to bottom (**Runtime → Run all**). The first cell installs any extra packages the notebook needs.

### Option B — Running locally

Use this option if you prefer VS Code or Jupyter on your own machine.

```bash
git clone https://github.com/ZYANZA/fins5557-applied-ai-finance.git
cd fins5557-applied-ai-finance
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install numpy pandas scipy scikit-learn matplotlib seaborn shap \
            streamlit google-generativeai anthropic jupyter
jupyter notebook
```

Python 3.10 or later is recommended. A few notebooks also install `torch`/`torchvision` when needed. Cells that read Colab secrets (`google.colab.userdata`) fall back to environment variables or mock mode when they run locally.

### API keys (optional; used for the live LLM features)

Notebooks from Week 3 onwards can call a live large language model. **A key is never required.** Without one, each notebook switches to a **mock simulation** that produces representative output, so you can still follow the whole pipeline.

To use the free Gemini tier:

1. Get a key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). No credit card is needed.
2. In Colab, click the **key icon** (Secrets panel in the left sidebar), choose **+ Add new secret**, name it `GOOGLE_API_KEY`, paste the key, and turn **Notebook access** on.
3. Re-run the setup cell. The notebook detects the secret automatically.

Some notebooks also accept Anthropic Claude or OpenAI keys, stored as secrets named `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`. When running locally, set these names as environment variables.

> Never paste API keys directly into notebook cells or commit them to Git.

### Streamlit apps (Weeks 6 and 9)

The Week 6 lab (`credit_app.py`, `robo_advisory_app.py`, `super_fund_app.py`) and the Week 9 case study (`advisory_app.py`) include interactive dashboards built with Streamlit.

- **In Colab:** the notebook writes the app file, starts it, and opens a public link through `pyngrok`. Follow the instructions in the notebook. A free [ngrok](https://ngrok.com) auth token is needed for this.
- **Locally:** run the app from inside its week folder, for example:
  ```bash
  cd week06
  streamlit run credit_app.py
  ```
  `credit_app.py` loads the trained model from `credit_pipeline.pkl`. If that file is missing, run the Week 6 notebook first to create it.

### Suggested study pattern

1. **Before the session:** skim the notebook's markdown and learning objectives.
2. **During the session:** run the cells along with the lecture and note where the output differs from what you expected.
3. **After the session:** complete the exercises and challenges at the end of each notebook. Change the parameters, data and prompts and observe what happens.
4. **For assessments:** use the notebooks as worked examples and reference implementations. Check the course Moodle page for the rules on using code and generative AI in assessed work.

---

## Weekly Materials

### Week 01 — AI and Data Literacy for Finance and Banking

| Notebook | Description |
|---|---|
| [week1-seminar.ipynb](week01/week1-seminar.ipynb) | AI methods in finance; credit scoring and customer segmentation; the data pipeline from raw financial data to model inputs |

**Key concepts:** ML taxonomy, supervised and unsupervised learning, data quality, the Digital Data Factory (DDF) pipeline, credit risk scoring.

### Week 02 — Applications, Opportunities and Limitations of AI

| Notebook | Description |
|---|---|
| [week2-seminar.ipynb](week02/week2-seminar.ipynb) | AI across the financial services value chain; limitations including hallucination, explainability gaps and model drift |

**Key concepts:** decision support systems, personalisation engines, real-time anomaly detection, AI regulation, responsible AI.

### Week 03 — Advanced Techniques in LLM and Multimodal Models

| Notebook | Description |
|---|---|
| [week3-seminar.ipynb](week03/week3-seminar.ipynb) | Transformer architecture, fine-tuning (LoRA), RAG, and multimodal models for earnings calls and document processing |

**Key concepts:** the attention mechanism, tokenisation, BloombergGPT, LoRA fine-tuning, retrieval-augmented generation, multimodal AI.

### Week 04 — AI Virtual Agents, AI Ethics and Use Cases

| Notebook | Description |
|---|---|
| [week4-seminar.ipynb](week04/week4-seminar.ipynb) | Agentic AI systems in finance; AI ethics (fairness, transparency, accountability); hands-on design of an agent that summarises financial reports |

**Key concepts:** agentic pipelines, tool use, multi-step reasoning, bias in financial AI, portfolio rebalancing agents.

### Week 05 — Banking Transformation

| Notebook | Description |
|---|---|
| [week5-seminar.ipynb](week05/week5-seminar.ipynb) | Digital transformation of banking and insurance; straight-through processing; AI-assisted underwriting; a full digitisation case study |

**Key concepts:** straight-through processing, intelligent document handling, AI underwriting, legacy migration, cloud adoption, model risk.

### Week 06 — Tech Lab

| File | Description |
|---|---|
| [week6-seminar.ipynb](week06/week6-seminar.ipynb) | Hands-on lab with the Python AI stack for finance: a credit risk classifier, earnings report parsing with LLMs, a backtesting loop, and coding challenges |
| [credit_app.py](week06/credit_app.py) | Streamlit credit-scoring app (uses `credit_pipeline.pkl`) |
| [robo_advisory_app.py](week06/robo_advisory_app.py) | Streamlit robo-advisory portfolio app |
| [super_fund_app.py](week06/super_fund_app.py) | Streamlit superannuation fund projection app |

**Key concepts:** `pandas`, `scikit-learn`, LLM APIs, backtesting, financial data wrangling, deploying models as apps. *This week is code-first and has less prose than the other weeks.*

### Week 07 — AI in Corporate Finance

| Notebook | Description |
|---|---|
| [week7-seminar.ipynb](week07/week7-seminar.ipynb) | AI-augmented valuation (DCF and comparable company analysis); NLP on financial filings; FP&A automation; board reporting |

**Key concepts:** sentiment extraction from filings, ML-based comparables, treasury cash forecasting, FP&A automation, the CFO's digital mandate.

### Week 08 — Trading and Investing with AI

| Notebook | Description |
|---|---|
| [week8-case-study.ipynb](week08/week8-case-study.ipynb) | Case study comparing an algorithmic trading platform with a long-term AI investment platform, covering design, governance and bias analysis |

**Key concepts:** algorithmic bias, mean-variance optimisation, RL-based allocation, factor models, high-frequency versus long-horizon strategies.

### Week 09 — AI Asset and Wealth Management

| File | Description |
|---|---|
| [week9-case-study.ipynb](week09/week9-case-study.ipynb) | End-to-end WealthTech platform simulation: client profiling, goals-based planning, portfolio construction, LLM-assisted SOA generation, and a best-interest-duty (BID) compliance gate |
| [advisory_app.py](week09/advisory_app.py) | Streamlit advisory dashboard |

**Key concepts:** robo-advice, goals-based investing, best-interest duty, superannuation AI, WealthTech architecture.

### Week 10 — Financial Intelligence

| Notebook | Description |
|---|---|
| [week10-case-study.ipynb](week10/week10-case-study.ipynb) | ESG compliance; financial inclusion through alternative credit scoring; alternative data (satellite, geospatial); AI-enabled fraud detection |

**Key concepts:** financial inclusion, alternative data, ESG scoring with FinBERT, greenwashing detection, deepfake fraud, the UN SDGs.

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

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Re-run the notebook's install cell, or `pip install <package>` locally |
| An LLM cell prints *mock mode* | No API key was found. Check that the secret name is exactly `GOOGLE_API_KEY` and that **Notebook access** is on |
| `429` / quota errors from Gemini | You have hit the free-tier rate limit. Wait a minute and re-run, or continue in mock mode |
| No public link appears for a Streamlit app in Colab | Add your ngrok auth token as the notebook instructs, then restart the app cell |
| Colab session reset | Runtimes are temporary. Re-run from the top; save your copy to Drive to keep your edits |

---

## Reference Textbooks

- Hilpisch, Y. (2021). *Artificial Intelligence in Finance: A Python-Based Guide*. O'Reilly.
- Alammar, J. & Grootendorst, M. (2024). *Hands-On Large Language Models: Language Understanding and Generation*. O'Reilly.
- Hric, J. & Lin, Y. (2026). *Applied Data Science in FinTech: Models, Tools, and Case Studies*. Routledge.

---

## Licence and Attribution

These materials are provided to students enrolled in **FINS3657** and **FINS5557** at UNSW Business School for educational use only. All data in the notebooks is synthetic or publicly available, and nothing here is financial advice. Please do not redistribute the materials without permission from the course author.

For questions, use the forums on your course's Moodle page or contact the course team through Moodle.
