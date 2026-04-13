# AI Response Evaluator

A Python tool that uses **LLM-as-a-judge** to automatically score AI responses across five quality dimensions. Feed it a set of (question, response, reference) triples and get back structured scores, a summary report, and an interactive dashboard.

---

## How the Judging Works

```
test_cases.json
  └─ user_message + ai_response + reference
          │
          ▼
    evaluator/judge.py
    (Claude Sonnet as judge)
          │
          ▼
   5 dimension scores (1–5)
   + reasoning text
          │
          ▼
   results/eval_results.csv
          │
       ┌──┴──┐
       ▼     ▼
   Excel    PDF
   report  report
          │
          ▼
   streamlit dashboard
```

---

## Scoring Dimensions

| Dimension | What it measures |
|-----------|-----------------|
| **Helpfulness** | Does the response actually address what the user asked? |
| **Accuracy** | Is the information correct relative to the reference answer? |
| **Coherence** | Is it well-structured and easy to understand? |
| **Tone** | Is the tone appropriate and professional? |
| **Overall** | Holistic assessment across all dimensions |

Scores are **1–5**. A score of **4 or above** counts as a Pass.

---

## Project Structure

```
ai-evaluator/
├── .env                        # API key and model config (never commit this)
├── requirements.txt            # Python dependencies
├── main.py                     # CLI entry point — runs eval + exports reports
├── dashboard.py                # Streamlit interactive dashboard
├── data/
│   └── test_cases.json         # Input: list of {user_message, ai_response, reference}
├── evaluator/
│   ├── __init__.py             # Package exports
│   ├── judge.py                # LLM-as-a-judge core logic (evaluate function)
│   ├── runner.py               # Batch loop — iterates cases, calls judge, saves CSV
│   ├── metrics.py              # Rich terminal summary table
│   └── exporter.py             # Excel (openpyxl) and PDF (reportlab) report generation
└── results/                    # Auto-generated outputs
    ├── eval_results.csv        # Raw scores for all test cases
    ├── eval_report.xlsx        # Excel workbook (3 sheets: Results, Summary, Worst Cases)
    └── eval_report.pdf         # PDF report with charts and worst-case breakdown
```

---

## Setup

**1. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure your API key**

Edit `.env` in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
EVAL_MODEL=claude-haiku-4-5-20251001
JUDGE_MODEL=claude-sonnet-4-6
```

**4. Add your test cases**

Edit `data/test_cases.json`. Each entry needs:
```json
{
  "id": "tc_001",
  "user_message": "What is the capital of France?",
  "ai_response": "Paris.",
  "reference": "Paris is the capital of France."
}
```

**5. Run the evaluation**
```bash
python main.py
```
This generates `results/eval_results.csv`, `eval_report.xlsx`, and `eval_report.pdf`.

**6. Open the dashboard**
```bash
streamlit run dashboard.py
```

---

## Dashboard Features

- **Overall Summary** — average score and pass rate card for each dimension
- **Score Distribution** — bar chart of average scores per dimension
- **Score Radar** — radar/spider chart across all five dimensions
- **Pass / Fail Ratio** — donut pie chart with total pass, total fail, and pass rate metrics
- **All Results Table** — filterable by minimum overall score, with ✅/❌ status badges and progress bars for scores
- **Worst Performing Cases** — expandable cards for the 3 lowest-scoring responses
- **Export Reports** — one-click generation and download of Excel and PDF reports

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| **Python 3.11+** | Runtime |
| **Anthropic SDK** | Claude API calls (judge + optional eval model) |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Bar chart, radar chart, donut pie chart |
| **pandas** | CSV loading, filtering, aggregation |
| **openpyxl** | Excel report generation |
| **reportlab** | PDF report generation |
| **rich** | Terminal progress bar and summary table |
| **matplotlib** | Chart images embedded in the PDF |

---

## Security Note

> **Never commit `.env` to GitHub.**
> Add `.env` to your `.gitignore` before pushing:
> ```
> echo ".env" >> .gitignore
> ```
> Your `ANTHROPIC_API_KEY` is a secret — anyone with it can make API calls billed to your account.
