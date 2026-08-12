# 🌾 AgriSaarthi

**AgriSaarthi** ("Agri-companion") is a full-stack agricultural advisory platform that gives farmers AI-driven crop recommendations, crop disease detection, and personalized government scheme eligibility — through a multilingual web app backed by a FastAPI service and a suite of trained ML and RAG pipelines.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Machine Learning Pipelines](#machine-learning-pipelines)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Roadmap](#roadmap)
- [Team](#team)

---

## Overview

AgriSaarthi combines three domain-specific AI systems behind a unified FastAPI backend and a React frontend, so a farmer can:

1. **Get a crop recommendation** based on soil, weather, and location — a tuned ML classifier with a RAG + LLM fallback for low-confidence or missing-data cases.
2. **Diagnose crop diseases** from a leaf photo using a trained CNN, enriched with treatment guidance retrieved from a curated agronomy knowledge base.
3. **Discover government schemes** they're eligible for (subsidies, credit, insurance, irrigation, etc.) via rule-based eligibility filtering plus semantic search over official scheme documents.

Built for real-world usability: a multilingual UI (English, Hindi, Marathi, Bengali, Kannada), persistent farmer profiles, and activity logging.

---

## Key Features

- 🌱 **Crop Recommendation Engine** — Optuna-tuned, cross-validated classifier (XGBoost, CatBoost, LightGBM, Random Forest, Extra Trees, HistGradientBoosting) trained on soil nutrients (N/P/K), climate, and soil type, with SHAP-based explainability.
- 🩺 **Disease Detection** — CNN-based leaf disease classifier with confidence-margin and entropy-based uncertainty rejection, paired with a knowledge base of disease treatments retrieved via embeddings.
- 🏛️ **Government Scheme Advisor** — Eligibility-rule engine combined with ChromaDB vector search across Indian agricultural schemes (PM-KISAN, PMFBY, KCC, PM-KUSUM, RKVY, and more).
- 🤖 **LLM-Powered Explanations** — Google Gemini synthesizes natural-language, farmer-friendly explanations from model + retrieval outputs.
- 👤 **Farmer Profiles & Activity History** — Persisted via SQLite, with profile auto-creation on first sign-in.
- 🌐 **Multilingual Frontend** — Full UI translations for English, Hindi, Marathi, Bengali, and Kannada.
- 🔌 **Confidence-Aware Fallbacks** — Crop and disease pipelines fall back to RAG when model confidence, margin, or entropy thresholds aren't met, instead of returning a low-quality prediction.

---

## Architecture

```
React Frontend (Vite)  ──REST──▶  FastAPI Backend (backend/main.py)
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
        Crop Router              Disease Router           Gov. Schemes Router
      /crop/recommend           /disease/analyze         /government-schemes/recommend
              │                         │                         │
        ML Classifier             CNN Model                Eligibility Rules
      (best_model.pkl)            (model.pth)               (eligibility_rules.json)
              │  low confidence?        │  low confidence?         │
              ▼                         ▼                         ▼
        RAG Retriever + Gemini    RAG Retriever + Gemini    ChromaDB Search + Gemini

  Shared: backend/services/db_service.py → SQLite (farmer profiles & activity logs)
```

Each domain follows the same pattern: a trained model produces a prediction with a confidence score; if that score (or a margin/entropy check) falls below threshold, the system falls back to retrieval-augmented generation over a curated knowledge base, with Gemini synthesizing the final farmer-facing explanation.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, Lucide Icons |
| **Backend** | FastAPI, Pydantic, Uvicorn |
| **ML / Data Science** | scikit-learn, XGBoost, CatBoost, LightGBM, Optuna, SHAP, PyTorch (CNN), pandas, NumPy |
| **RAG / LLM** | ChromaDB (vector store), Sentence-Transformers (embeddings), Google Gemini (`google-genai`) |
| **Storage** | SQLite (farmer profiles & activity logs) |

---

## Repository Structure

```
AgriSaarthi/
├── ai/
│   ├── crop_recommendation/     # ML training pipeline, models, reports, knowledge base
│   ├── disease_detection/       # CNN model, disease knowledge base, inference
│   └── government_schemes/      # scheme documents, eligibility rules, embeddings
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── routers/                 # crop, disease, government_schemes, farmer endpoints
│   └── services/                # RAG retrievers, Gemini service, DB, weather, soil, location
├── frontend/
│   └── src/                     # pages, components, api client, context, translations
├── src/                         # shared dataset/model/utility helpers
├── tests/                       # pytest suite
├── predict.py / train.py        # top-level training & prediction scripts
├── requirements.txt             # backend/ML Python dependencies
└── .env.example                 # required environment variables
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Backend Setup

```bash
git clone https://github.com/singhalsharvi/AgriSaarthi.git
cd AgriSaarthi

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# edit .env and set GEMINI_API_KEY=your_actual_key

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

API available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000` and proxies `/api` requests to the backend at `http://127.0.0.1:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET`  | `/` | Health/service info |
| `GET`  | `/health` | Health check |
| `POST` | `/crop/recommend` | Recommend crops from soil/weather/location inputs (ML + RAG fallback) |
| `POST` | `/disease/analyze` | Analyze crop disease from an uploaded leaf image or text query |
| `POST` | `/disease/detect` | Disease detection endpoint |
| `POST` | `/government-schemes/recommend` | Recommend eligible government schemes for a farmer profile |
| `POST` | `/farmer/profile` | Create or update a farmer profile |
| `GET`  | `/farmer/profile/{farmer_id}` | Retrieve a farmer profile (auto-creates a default if missing) |

Full request/response schemas are available via the Swagger UI at `/docs`.

---

## Machine Learning Pipelines

### 🌱 Crop Recommendation (`ai/crop_recommendation`)
- **Target**: 22 crop classes (rice, maize, cotton, banana, coffee, etc.)
- **Features**: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall, Soil Type
- **Models compared**: XGBoost, CatBoost, LightGBM, Random Forest, Extra Trees, HistGradientBoosting
- **Optimization**: Optuna (TPE sampler), 5-fold stratified cross-validation, 20% stratified holdout
- **Explainability**: SHAP summary plots, feature-importance diagnostics
- Train: `python ai/crop_recommendation/main.py`
- Infer: `ai.crop_recommendation.prediction.predict_crop(...)`

### 🩺 Disease Detection (`ai/disease_detection`)
- CNN model (`model.pth`) trained on crop leaf images (tomato, potato, pepper varieties)
- Confidence gating using top-1 confidence, confidence margin, and normalized entropy thresholds to reject uncertain predictions
- Falls back to a knowledge base of disease treatments retrieved via sentence-transformer embeddings

### 🏛️ Government Schemes (`ai/government_schemes`)
- Rule-based eligibility filter (`eligibility_rules.json`) checked against farmer category, income, landholding, age, and gender
- Semantic retrieval over scheme documents (PM-KISAN, PMFBY, KCC, PM-KUSUM, RKVY, NMSA, PMFME, and more) using ChromaDB
- Gemini synthesizes eligible schemes into a clear, farmer-facing explanation

---

## Testing

The `tests/` directory contains a pytest suite covering confidence-based fallback logic, disease detection, farmer-profile flows, location-aware crop RAG retrieval, and the end-to-end RAG pipeline.

```bash
python -m unittest discover
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key for Google Gemini, used to generate natural-language explanations across all three advisory domains. Get one at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey). |

Copy `.env.example` to `.env` and populate it before running the backend.

---

## Roadmap

- [ ] Live weather API integration for real-time climate inputs
- [ ] Expanded disease model coverage beyond current crop varieties
- [ ] Mobile app / offline-first support for low-connectivity rural areas
- [ ] Additional regional language translations

---

## Team

AgriSaarthi was built by a team of three:

- **Sharvi Singhal** — IGDTUW
- **Trisha Jha** — IGDTUW
- **Ishika Garg** — NSUT

---

*Built to help farmers make faster, more informed decisions about what to grow, how to protect it, and which government support they can access.*
