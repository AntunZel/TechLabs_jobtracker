# Career Prediction System — Setup Guide

## Project structure

```
career_predictor/
├── train_model.py        # Synthetic data generation + model training
├── server.py             # FastAPI backend (prediction + LLM streaming)
├── requirements.txt      # Python dependencies
├── models/               # Saved model artifact (created after training)
│   └── career_model.pkl
├── data/                 # Synthetic dataset (created after training)
│   └── synthetic_training_data.csv
└── static/
    └── index.html        # Frontend — open this in the browser
```

---

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Train the model

This generates 3 000 synthetic profiles (300 per job role) and trains
the XGBoost + MLP ensemble. Takes ~30–60 seconds.

```bash
python train_model.py
```

You will see:
- A classification report with per-class precision / recall
- Top-3 accuracy across the 10 career roles
- Confirmation that `models/career_model.pkl` was saved

---

## 3. Set your Anthropic API key - only if you're using the "server.py" file - the one with paid API - currently doesn't work

The LLM suggestion endpoint needs a valid API key.
Get one at https://console.anthropic.com

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 4. Start the backend server

```bash
uvicorn server:app --reload --port 8000
```
or
```bash
uvicorn server_noapi:app --reload --port 8000
```

The API is now live at http://localhost:8000
Auto-generated docs: http://localhost:8000/docs

---

## 5. Open the website

Open `static/index.html` directly in your browser, or serve it via the FastAPI
static mount at:

```
http://localhost:8000/static/index.html
```

---

## API endpoints

| Method | Endpoint    | Description                              |
|--------|-------------|------------------------------------------|
| GET    | /health     | Liveness check                           |
| POST   | /predict    | Run ML model → returns top-5 predictions |
| POST   | /suggest    | Stream LLM career advice (SSE)           |
| GET    | /docs       | Swagger UI (auto-generated)              |

### Example /predict request body

```json
{
  "education": "master",
  "field_of_study": "data_science",
  "years_experience": 3.5,
  "tech_skills": ["python", "ml", "sql", "cloud"],
  "soft_skills": ["analytical", "problemsolving", "communication"],
  "work_pref": "hybrid",
  "industry": "tech",
  "salary_priority": "balanced",
  "statement": "I enjoy building data pipelines and running experiments."
}
```

---

## How the model works

```
User profile
    │
    ▼
Feature engineering
  • Label-encode categoricals (education, field, work_pref, …)
  • Multi-hot encode skill arrays (tech_skills, soft_skills)
  • StandardScale continuous features (years_experience)
    │
    ▼
Soft-voting ensemble (weights: XGBoost 60%, MLP 40%)
  ┌──────────────────┬──────────────────────────────────┐
  │ XGBoost          │ MLP (128 → 64 → 32 → softmax)   │
  │ n_estimators=300 │ activation=relu, early_stopping  │
  │ max_depth=6      │ solver=adam                      │
  └──────────────────┴──────────────────────────────────┘
    │
    ▼
class_probabilities[10 roles]  →  top-5 ranked predictions
    │
    ▼ (profile + predictions passed as context)
Anthropic claude-sonnet-4  →  streamed career advice (SSE)
```

## Replacing synthetic data with real data

Edit `train_model.py` and replace the `build_dataset()` call with:

```python
df = pd.read_csv("data/your_real_data.csv")
```

Your CSV must have these columns:
- `education`, `field_of_study`, `years_experience`
- `tech_skills`  (Python list stored as JSON string, e.g. `'["python","sql"]'`)
- `soft_skills`  (same format)
- `work_pref`, `industry`, `salary_priority`
- `job_role`  (the target label — must match the JOB_ROLES list or update it)
