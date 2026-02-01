# Data Reliability Audit Engine

A deterministic, explainable, and privacy-preserving system for auditing dataset reliability before any machine learning is applied.

This project performs a structural and statistical audit of tabular datasets and produces:

- A machine-verifiable audit report (authoritative)
- A human-readable explanation layer (non-authoritative, optional, LLM-powered)

The system is designed to surface data risks early, before modeling decisions lock in hidden failure modes.

---

## Why This Exists

Most ML failures originate in data, not models.

This engine is built to:

- Detect structural risks such as leakage, duplication, constant or near-constant features
- Explicitly surface unassessed uncertainty (unknowns that cannot be evaluated)
- Preserve epistemic humility by separating deterministic audit logic from AI explanations
- Scale from small CSVs to large, high-dimensional datasets

No AutoML.
No silent assumptions.
No black-box decisions.

---

## System Architecture

Backend (Python, FastAPI):

- Deterministic audit pipeline
- Risk diagnostics (structural, statistical, metadata-based)
- Explicit decision trace
- Optional LLM explanation layer (local-first via Ollama)

Frontend (React + Vite):

- Clean audit UI
- Zone-based explanation rendering
- Raw audit evidence viewer
- Audience-aware explanation display (Engineer / Executive / Auditor)

Explanation Layer:

- Strictly non-authoritative
- Plain-text only
- Explains detected risks and unassessed uncertainty
- Never introduces new conclusions

---

## Key Design Principles

- Deterministic core, probabilistic explanation
- Human-in-the-loop by design
- Privacy-first (local LLM support)
- Large-dataset safe (summarization before explanation)
- Failure-aware instead of accuracy-obsessed

---

## Features

- Structural risk detection (ID-like columns, duplicates, constant features, near-constant features)
- Explicit unassessed risk channels (label provenance, temporal context, problem definition)
- Decision output: pass / fix / block
- Audience-aware explanations
- Raw audit evidence always visible
- Works on datasets with 100k+ rows and ~100 columns

---

## Local Setup

### Backend

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
uvicorn draudit.backend.main:app --reload
