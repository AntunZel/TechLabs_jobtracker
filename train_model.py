"""
train_model.py
==============
Generates synthetic training data, trains an XGBoost + MLP ensemble,
and saves the pipeline to models/career_model.pkl

Run once before starting the server:
    python train_model.py
"""

import json
import pickle
import random
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import xgboost as xgb
from sklearn.ensemble import VotingClassifier
from feature_engineering import FeatureEngineer

random.seed(42)
np.random.seed(42)

# ── 1. Define the label space ────────────────────────────────────────────────

JOB_ROLES = [
    "Data Scientist",
    "Machine Learning Engineer",
    "Software Engineer",
    "Data Analyst",
    "Product Manager",
    "UX/UI Designer",
    "DevOps / Cloud Engineer",
    "Business Analyst",
    "Cybersecurity Analyst",
    "Full-Stack Developer",
]

# ── 2. Feature definitions ───────────────────────────────────────────────────

EDUCATION_LEVELS = ["high_school", "associate", "bachelor", "master", "phd", "bootcamp"]
FIELDS_OF_STUDY  = ["cs", "data_science", "engineering", "business", "design",
                     "natural_sci", "social_sci", "humanities", "medicine", "law", "other"]
TECH_SKILLS      = ["python", "sql", "ml", "js", "cloud", "excel", "bi", "java",
                     "design_tools", "devops", "stats"]
SOFT_SKILLS      = ["leadership", "communication", "analytical", "creativity",
                     "teamwork", "problemsolving", "sales", "detail"]
WORK_PREFS       = ["remote", "hybrid", "office"]
INDUSTRIES       = ["tech", "finance", "healthcare", "ecommerce", "media", "gov",
                     "consulting", "open"]
SALARY_OPTS      = ["high", "balanced", "impact"]

# ── 3. Role profile templates (probability weights for each feature) ─────────
# These guide synthetic data generation so it reflects realistic patterns.

ROLE_PROFILES = {
    "Data Scientist": {
        "edu": {"master": 0.4, "phd": 0.25, "bachelor": 0.25, "bootcamp": 0.1},
        "field": {"data_science": 0.4, "cs": 0.25, "natural_sci": 0.15, "engineering": 0.1, "other": 0.1},
        "tech_must": ["python", "ml", "stats", "sql"],
        "tech_optional": ["cloud", "bi"],
        "soft_must": ["analytical", "problemsolving"],
        "soft_optional": ["communication", "detail"],
        "exp_mean": 4.0, "exp_std": 2.5,
    },
    "Machine Learning Engineer": {
        "edu": {"master": 0.35, "phd": 0.2, "bachelor": 0.3, "bootcamp": 0.15},
        "field": {"cs": 0.35, "data_science": 0.3, "engineering": 0.2, "other": 0.15},
        "tech_must": ["python", "ml", "cloud"],
        "tech_optional": ["devops", "stats", "sql"],
        "soft_must": ["analytical", "problemsolving"],
        "soft_optional": ["teamwork", "detail"],
        "exp_mean": 4.5, "exp_std": 2.5,
    },
    "Software Engineer": {
        "edu": {"bachelor": 0.45, "master": 0.2, "bootcamp": 0.25, "associate": 0.1},
        "field": {"cs": 0.5, "engineering": 0.2, "other": 0.2, "bootcamp": 0.1},
        "tech_must": ["python", "java", "js"],
        "tech_optional": ["cloud", "devops", "sql"],
        "soft_must": ["problemsolving", "teamwork"],
        "soft_optional": ["communication", "detail"],
        "exp_mean": 3.5, "exp_std": 3.0,
    },
    "Data Analyst": {
        "edu": {"bachelor": 0.5, "master": 0.3, "associate": 0.1, "bootcamp": 0.1},
        "field": {"business": 0.3, "data_science": 0.2, "social_sci": 0.2, "cs": 0.15, "other": 0.15},
        "tech_must": ["sql", "excel", "bi"],
        "tech_optional": ["python", "stats"],
        "soft_must": ["analytical", "detail"],
        "soft_optional": ["communication", "problemsolving"],
        "exp_mean": 3.0, "exp_std": 2.5,
    },
    "Product Manager": {
        "edu": {"bachelor": 0.4, "master": 0.4, "phd": 0.1, "other": 0.1},
        "field": {"business": 0.35, "cs": 0.2, "social_sci": 0.2, "engineering": 0.15, "other": 0.1},
        "tech_must": ["excel"],
        "tech_optional": ["sql", "bi", "python"],
        "soft_must": ["leadership", "communication", "problemsolving"],
        "soft_optional": ["analytical", "creativity"],
        "exp_mean": 5.0, "exp_std": 3.0,
    },
    "UX/UI Designer": {
        "edu": {"bachelor": 0.45, "bootcamp": 0.25, "associate": 0.15, "master": 0.15},
        "field": {"design": 0.5, "cs": 0.15, "humanities": 0.15, "social_sci": 0.1, "other": 0.1},
        "tech_must": ["design_tools"],
        "tech_optional": ["js", "python"],
        "soft_must": ["creativity", "communication", "detail"],
        "soft_optional": ["teamwork", "analytical"],
        "exp_mean": 3.0, "exp_std": 2.5,
    },
    "DevOps / Cloud Engineer": {
        "edu": {"bachelor": 0.4, "master": 0.2, "bootcamp": 0.25, "associate": 0.15},
        "field": {"cs": 0.45, "engineering": 0.25, "other": 0.3},
        "tech_must": ["cloud", "devops"],
        "tech_optional": ["python", "java", "sql"],
        "soft_must": ["problemsolving", "detail"],
        "soft_optional": ["teamwork", "communication"],
        "exp_mean": 4.0, "exp_std": 2.5,
    },
    "Business Analyst": {
        "edu": {"bachelor": 0.5, "master": 0.35, "associate": 0.1, "other": 0.05},
        "field": {"business": 0.45, "social_sci": 0.2, "cs": 0.15, "other": 0.2},
        "tech_must": ["excel", "sql"],
        "tech_optional": ["bi", "python"],
        "soft_must": ["analytical", "communication", "detail"],
        "soft_optional": ["problemsolving", "leadership"],
        "exp_mean": 4.0, "exp_std": 2.5,
    },
    "Cybersecurity Analyst": {
        "edu": {"bachelor": 0.45, "master": 0.25, "bootcamp": 0.2, "associate": 0.1},
        "field": {"cs": 0.5, "engineering": 0.2, "other": 0.3},
        "tech_must": ["java", "cloud", "devops"],
        "tech_optional": ["python", "sql"],
        "soft_must": ["analytical", "detail", "problemsolving"],
        "soft_optional": ["communication", "teamwork"],
        "exp_mean": 4.0, "exp_std": 2.5,
    },
    "Full-Stack Developer": {
        "edu": {"bachelor": 0.4, "bootcamp": 0.35, "master": 0.15, "associate": 0.1},
        "field": {"cs": 0.45, "engineering": 0.2, "other": 0.35},
        "tech_must": ["js", "sql", "python"],
        "tech_optional": ["cloud", "devops", "java"],
        "soft_must": ["problemsolving", "teamwork"],
        "soft_optional": ["communication", "creativity"],
        "exp_mean": 3.5, "exp_std": 2.5,
    },
}


def sample_from_weights(weight_dict, fallback_list):
    """Sample one key from a dict of {key: probability}."""
    keys   = list(weight_dict.keys())
    probs  = np.array(list(weight_dict.values()), dtype=float)
    probs /= probs.sum()
    return np.random.choice(keys, p=probs)


def generate_sample(role: str) -> dict:
    """Generate one synthetic training sample for a given role."""
    profile = ROLE_PROFILES[role]

    edu   = sample_from_weights(profile["edu"], EDUCATION_LEVELS)
    field = sample_from_weights(profile["field"], FIELDS_OF_STUDY)
    exp   = max(0.0, np.random.normal(profile["exp_mean"], profile["exp_std"]))
    exp   = round(min(exp, 30.0), 1)

    # Tech skills: always include must-have, randomly sample optionals
    tech = list(profile["tech_must"])
    for s in profile["tech_optional"]:
        if random.random() < 0.55:
            tech.append(s)
    # Add a couple of random skills with low probability
    for s in TECH_SKILLS:
        if s not in tech and random.random() < 0.12:
            tech.append(s)

    # Soft skills
    soft = list(profile["soft_must"])
    for s in profile["soft_optional"]:
        if random.random() < 0.6:
            soft.append(s)
    for s in SOFT_SKILLS:
        if s not in soft and random.random() < 0.15:
            soft.append(s)

    work_pref = random.choice(WORK_PREFS)
    industry  = random.choice(INDUSTRIES)
    salary    = random.choice(SALARY_OPTS)

    return {
        "education": edu,
        "field_of_study": field,
        "years_experience": exp,
        "tech_skills": sorted(set(tech)),
        "soft_skills": sorted(set(soft)),
        "work_pref": work_pref,
        "industry": industry,
        "salary_priority": salary,
        "job_role": role,
    }


# ── 4. Generate dataset ──────────────────────────────────────────────────────

def build_dataset(samples_per_role: int = 300) -> pd.DataFrame:
    rows = []
    for role in JOB_ROLES:
        for _ in range(samples_per_role):
            rows.append(generate_sample(role))
    df = pd.DataFrame(rows)
    df.to_csv("data/synthetic_training_data.csv", index=False)
    print(f"✓ Generated {len(df)} samples across {len(JOB_ROLES)} roles")
    return df


# ── 5. Feature engineering ───────────────────────────────────────────────────




# ── 6. Build & train the ensemble ────────────────────────────────────────────

def train(df: pd.DataFrame):
    fe = FeatureEngineer()
    X  = fe.fit_transform(df)

    le = LabelEncoder()
    y  = le.fit_transform(df["job_role"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )

    # XGBoost — great at tabular structured features
    xgb_clf = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
        verbosity=0,
    )

    # MLP — captures non-linear feature interactions
    mlp_clf = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation="relu",
        solver="adam",
        max_iter=500,
        early_stopping=True,
        random_state=42,
        learning_rate_init=0.001,
    )

    # Soft-voting ensemble: averages class probabilities
    ensemble = VotingClassifier(
        estimators=[("xgb", xgb_clf), ("mlp", mlp_clf)],
        voting="soft",
        weights=[0.6, 0.4],   # XGBoost weighted slightly higher for tabular data
    )

    print("Training ensemble (XGBoost + MLP)…")
    ensemble.fit(X_train, y_train)

    # Evaluation
    y_pred = ensemble.predict(X_test)
    print("\n── Evaluation on held-out test set ──")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Top-3 accuracy
    proba       = ensemble.predict_proba(X_test)
    top3_hits   = sum(y_test[i] in np.argsort(proba[i])[-3:] for i in range(len(y_test)))
    top3_acc    = top3_hits / len(y_test)
    print(f"Top-3 accuracy: {top3_acc:.1%}")

    # Save everything needed for inference
    artifact = {
        "ensemble":          ensemble,
        "feature_engineer":  fe,
        "label_encoder":     le,
        "job_roles":         JOB_ROLES,
        "tech_skills":       TECH_SKILLS,
        "soft_skills":       SOFT_SKILLS,
        "education_levels":  EDUCATION_LEVELS,
        "fields_of_study":   FIELDS_OF_STUDY,
    }
    Path("models").mkdir(exist_ok=True)
    with open("models/career_model.pkl", "wb") as f:
        pickle.dump(artifact, f)
    print("\n✓ Model saved to models/career_model.pkl")
    return artifact


if __name__ == "__main__":
    print("=== Career Prediction Model — Training ===\n")
    df = build_dataset(samples_per_role=300)
    train(df)
    print("\nDone. Run:  uvicorn server:app --reload")
