"""
server.py
=========
FastAPI backend — serves the ML model and generates career suggestions
without any external API (no cost, no API key needed).

Start with:
    uvicorn server:app --reload --port 8000

NOTE: To switch to real Anthropic LLM suggestions later, see the comment
block at the bottom of this file marked "OPTIONAL: Anthropic upgrade".
"""

import json
import pickle
import time
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from code_files_Antun.feature_engineering import FeatureEngineer



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

# ── FastAPI app ──────────────────────────────────────────────────────────────

app = FastAPI(title="Career Prediction API", version="1.0.0")

@app.get("/")
def root():
    return FileResponse("static/index.html")

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
#app.mount("/", StaticFiles(directory="static", html=True), name="static")


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
    Stream rule-based career suggestions — no API key or cost required.
    Uses the ML prediction + profile to build specific, personalised advice.

    The SSE format is identical to the Anthropic version so the frontend
    requires zero changes.  See the bottom of this file to swap in the
    real LLM when you have an API key.
    """
    try:
        X = feature_engineer.transform_single(profile.model_dump())
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    proba    = ensemble.predict_proba(X)[0]
    top3_idx = np.argsort(proba)[::-1][:3]
    top_roles = [label_encoder.classes_[i] for i in top3_idx]
    top_role  = top_roles[0]

    text = _build_suggestion(profile, top_role, top_roles)

    def stream_chars():
        """Emit one character at a time so the frontend typewriter effect works."""
        for char in text:
            payload = json.dumps({"chunk": char})
            yield f"data: {payload}\n\n"
            time.sleep(0.008)          # ~125 chars/sec — feels like live typing
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_chars(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Rule-based suggestion builder ────────────────────────────────────────────

# Per-role advice: next step + skill gap + resource
_ROLE_ADVICE = {
    "Data Scientist": {
        "next_step": "Build a end-to-end portfolio project — pick a public dataset (Kaggle works well), train a model, and deploy it with a simple API.",
        "skill_gap": "MLOps fundamentals (experiment tracking, model versioning)",
        "resource": "MLflow docs or the free *Full Stack Deep Learning* course at fullstackdeeplearning.com",
    },
    "Machine Learning Engineer": {
        "next_step": "Contribute to an open-source ML library (Hugging Face, scikit-learn) or build a model-serving project using FastAPI + Docker.",
        "skill_gap": "Containerisation and model deployment at scale",
        "resource": "Docker's official *Get Started* guide + the *Deploying ML Models* section on Towards Data Science",
    },
    "Software Engineer": {
        "next_step": "Build and publish a small open-source tool on GitHub — even a CLI utility demonstrates initiative to hiring managers.",
        "skill_gap": "System design fundamentals (databases, APIs, caching)",
        "resource": "*Designing Data-Intensive Applications* by Martin Kleppmann — widely regarded as the best single book on the topic",
    },
    "Data Analyst": {
        "next_step": "Create a public Tableau Public or Power BI dashboard on a topic you care about and share it on LinkedIn.",
        "skill_gap": "SQL window functions and advanced aggregations",
        "resource": "Mode Analytics SQL Tutorial (free) or *Learning SQL* by Alan Beaulieu",
    },
    "Product Manager": {
        "next_step": "Write a product teardown of an app you use daily — document the user problem, existing solution, and one improvement. Share it publicly.",
        "skill_gap": "Quantitative analysis and A/B testing fundamentals",
        "resource": "Reforge's free resources or *Inspired* by Marty Cagan",
    },
    "UX/UI Designer": {
        "next_step": "Do a unsolicited redesign of an existing product (a common interview piece), document your process, and add it to a Behance or Dribbble portfolio.",
        "skill_gap": "Usability testing and research synthesis",
        "resource": "Nielsen Norman Group's free articles at nngroup.com — the industry standard reference",
    },
    "DevOps / Cloud Engineer": {
        "next_step": "Get the AWS Cloud Practitioner or Google Associate Cloud Engineer certification — it's widely recognised and achievable in 4–6 weeks of study.",
        "skill_gap": "Infrastructure-as-code (Terraform or Pulumi)",
        "resource": "HashiCorp's free Terraform tutorials at developer.hashicorp.com",
    },
    "Business Analyst": {
        "next_step": "Shadow or interview a domain expert, document a business process as a BPMN diagram, and identify one inefficiency with a proposed fix.",
        "skill_gap": "Data storytelling and executive communication",
        "resource": "Cole Nussbaumer Knaflic's *Storytelling with Data* (book + free blog)",
    },
    "Cybersecurity Analyst": {
        "next_step": "Set up a home lab (VirtualBox is free), practice on TryHackMe or HackTheBox, and work toward the CompTIA Security+ certification.",
        "skill_gap": "Network forensics and log analysis",
        "resource": "TryHackMe.com — free learning paths for beginners and intermediates",
    },
    "Full-Stack Developer": {
        "next_step": "Build and deploy a full-stack side project (e.g. a SaaS tool or productivity app) — live URLs impress more than code alone.",
        "skill_gap": "Database optimisation and backend performance",
        "resource": "Postgres documentation + *The Art of PostgreSQL* for deeper SQL knowledge",
    },
}

_EDU_LABELS = {
    "high_school": "a high school background",
    "associate":   "an associate degree",
    "bachelor":    "a bachelor's degree",
    "master":      "a master's degree",
    "phd":         "a PhD",
    "bootcamp":    "a bootcamp / self-taught background",
}

_FIELD_LABELS = {
    "cs":          "computer science",
    "data_science":"data science / statistics",
    "engineering": "engineering",
    "business":    "business / management",
    "design":      "design / arts",
    "natural_sci": "natural sciences",
    "social_sci":  "social sciences",
    "humanities":  "humanities / languages",
    "medicine":    "medicine / health",
    "law":         "law",
    "other":       "a multidisciplinary background",
}


def _build_suggestion(profile: ProfileInput, top_role: str, top_roles: list) -> str:
    edu       = _EDU_LABELS.get(profile.education, profile.education)
    field     = _FIELD_LABELS.get(profile.field_of_study, profile.field_of_study)
    exp_years = int(profile.years_experience)
    exp_str   = f"{exp_years} year{'s' if exp_years != 1 else ''}"
    techs     = profile.tech_skills
    softs     = profile.soft_skills
    advice    = _ROLE_ADVICE.get(top_role, _ROLE_ADVICE["Software Engineer"])

    # Section 1 — Why these roles fit
    tech_str  = ", ".join(techs[:4]) if techs else "your general background"
    soft_str  = " and ".join(softs[:2]) if softs else "your soft skills"
    others    = " and ".join(top_roles[1:3]) if len(top_roles) > 1 else ""
    others_line = f" Roles like **{others}** also align closely with your profile." if others else ""

    section1 = (
        f"## Why these roles fit you\n\n"
        f"With {edu} in {field} and {exp_str} of experience, your profile maps "
        f"well to **{top_role}** — particularly because of your skills in {tech_str} "
        f"and strengths in {soft_str}.{others_line}\n\n"
    )

    # Section 2 — Next step
    section2 = (
        f"## Your recommended next step\n\n"
        f"{advice['next_step']}\n\n"
    )

    # Section 3 — Skill to develop
    section3 = (
        f"## A skill to develop\n\n"
        f"The most impactful gap to close right now is **{advice['skill_gap']}**. "
        f"A good starting point: {advice['resource']}.\n"
    )

    return section1 + section2 + section3


# ─────────────────────────────────────────────────────────────────────────────
# OPTIONAL: Anthropic upgrade
# ─────────────────────────────────────────────────────────────────────────────
# When you have an API key, replace the entire /suggest endpoint above with:
#
#   import anthropic
#   client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
#
#   @app.post("/suggest")
#   def suggest(profile: ProfileInput):
#       X        = feature_engineer.transform_single(profile.model_dump())
#       proba    = ensemble.predict_proba(X)[0]
#       top3_idx = np.argsort(proba)[::-1][:3]
#       top_roles = [f"{label_encoder.classes_[i]} ({round(proba[i]*100,1)}%)" for i in top3_idx]
#
#       def stream_response():
#           with client.messages.stream(
#               model="claude-haiku-4-5-20251001",   # cheapest model
#               max_tokens=600,
#               system="You are a career advisor. Give warm, specific advice in 3 sections: "
#                      "why these roles fit, the recommended next step, and a skill gap to close. "
#                      "Use markdown. 2-3 sentences per section.",
#               messages=[{"role": "user", "content":
#                   f"Profile: {profile.model_dump()}\nTop predicted roles: {', '.join(top_roles)}"}],
#           ) as stream:
#               for chunk in stream.text_stream:
#                   yield f"data: {json.dumps({'chunk': chunk})}\n\n"
#           yield "data: [DONE]\n\n"
#
#       return StreamingResponse(stream_response(), media_type="text/event-stream",
#                                headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
# ─────────────────────────────────────────────────────────────────────────────
