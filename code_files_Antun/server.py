"""
server.py
=========
FastAPI backend — serves the ML model and streams LLM suggestions.

Start with:
    uvicorn server:app --reload --port 8000
"""

import json
import pickle
import asyncio
from pathlib import Path
from typing import List, Optional
from code_files_Antun.feature_engineering import FeatureEngineer

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import anthropic
import pandas as pd

# ── Load model artifact once at startup ─────────────────────────────────────


MODEL_PATH = Path("models/career_model.pkl")

if not MODEL_PATH.exists():
    raise RuntimeError(
        "Model file not found. Run `python train_model.py` first."
    )

with open(MODEL_PATH, "rb") as f:
    artifact = pickle.load(f)

ensemble         = artifact["ensemble"]
feature_engineer = artifact["feature_engineer"]
label_encoder    = artifact["label_encoder"]
JOB_ROLES        = artifact["job_roles"]

print("✓ Model loaded successfully")

# ── Anthropic client ─────────────────────────────────────────────────────────
# Set your API key as an environment variable:
#   export ANTHROPIC_API_KEY="sk-ant-..."
# Or pass it directly (not recommended for production):
#   client = anthropic.Anthropic(api_key="sk-ant-...")

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

# ── FastAPI app ──────────────────────────────────────────────────────────────

app = FastAPI(title="Career Prediction API", version="1.0.0")

# Allow requests from the frontend (localhost during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend from the static/ folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Request / Response schemas ───────────────────────────────────────────────

class ProfileInput(BaseModel):
    education:        str
    field_of_study:   str
    years_experience: float
    tech_skills:      List[str]
    soft_skills:      List[str]
    work_pref:        Optional[str] = "hybrid"
    industry:         Optional[str] = "open"
    salary_priority:  Optional[str] = "balanced"
    statement:        Optional[str] = ""


class PredictedRole(BaseModel):
    rank:        int
    title:       str
    probability: float    # 0–100 %
    confidence:  str      # "High" | "Medium" | "Low"


class PredictionResponse(BaseModel):
    top_roles:      List[PredictedRole]
    profile_summary: dict


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "model": "career_ensemble_v1"}


@app.post("/predict", response_model=PredictionResponse)
def predict(profile: ProfileInput):
    """
    Run the ML ensemble and return the top-5 predicted career roles
    with their probability scores.
    """
    try:
        X = feature_engineer.transform_single(profile.model_dump())
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Feature engineering failed: {e}")

    proba  = ensemble.predict_proba(X)[0]           # shape: (n_classes,)
    top5_idx = np.argsort(proba)[::-1][:5]

    results = []
    for rank, idx in enumerate(top5_idx, start=1):
        pct = round(float(proba[idx]) * 100, 1)
        results.append(PredictedRole(
            rank=rank,
            title=label_encoder.classes_[idx],
            probability=pct,
            confidence="High" if pct >= 30 else ("Medium" if pct >= 15 else "Low"),
        ))

    return PredictionResponse(
        top_roles=results,
        profile_summary={
            "education":        profile.education,
            "field_of_study":   profile.field_of_study,
            "years_experience": profile.years_experience,
            "tech_skills":      profile.tech_skills,
            "soft_skills":      profile.soft_skills,
        },
    )


@app.post("/suggest")
def suggest(profile: ProfileInput):
    """
    Stream personalised career suggestions from Claude based on the
    user's profile and predicted top role. Returns an SSE stream.
    """
    # First run the prediction to pass context to the LLM
    try:
        X = feature_engineer.transform_single(profile.model_dump())
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    proba    = ensemble.predict_proba(X)[0]
    top3_idx = np.argsort(proba)[::-1][:3]
    top_roles = [
        f"{label_encoder.classes_[i]} ({round(proba[i]*100, 1)}%)"
        for i in top3_idx
    ]

    system_prompt = """You are a career advisor embedded in a job-prediction tool.
You will receive a candidate's background and the model's top predicted roles.
Your job is to give warm, specific, actionable advice in 3 clear sections:

1. **Why these roles fit you** — connect their specific skills/background to the predictions
2. **Your recommended next step** — one concrete action (course, certification, project, or application strategy)
3. **A skill to develop** — the single most impactful gap to close, with a specific resource

Be concise, direct, and encouraging. Use markdown formatting. 2–3 sentences per section max."""

    user_content = f"""
Candidate profile:
- Education: {profile.education} in {profile.field_of_study}
- Experience: {profile.years_experience} years
- Technical skills: {', '.join(profile.tech_skills) or 'none listed'}
- Soft skills: {', '.join(profile.soft_skills) or 'none listed'}
- Work preference: {profile.work_pref}
- Industry interest: {profile.industry}
- Personal note: {profile.statement or '(none provided)'}

Model predicted top roles: {', '.join(top_roles)}

Provide personalised career suggestions.
"""

    def stream_response():
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        ) as stream:
            for text_chunk in stream.text_stream:
                # SSE format: each chunk is "data: <content>\n\n"
                payload = json.dumps({"chunk": text_chunk})
                yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
