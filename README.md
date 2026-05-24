# 🚀 Career Recommendation System

An intelligent and explainable career recommendation system built with Python and Streamlit.

This project analyzes a candidate’s:
- technical skills
- soft skills
- preferred career roles
- experience
- education
- English language level
- Danish language level
- preferred locations
- preferred employment types
- preferred work modes

and recommends the best matching career opportunities using a hybrid recommendation engine.

---

# 📌 Project Goal

The goal of this project is to help candidates discover career opportunities that best match their profile through an explainable and data-driven recommendation system.

The system:
- analyzes the candidate profile
- evaluates technical and soft skill compatibility
- performs career match analysis
- identifies missing skills and skill gaps
- generates a personalized success roadmap
- provides interactive decision-support visual analytics

to help users better understand:
- their strengths
- weaknesses
- market readiness
- learning priorities
- best matching career opportunities

---

# 🧠 Recommendation System Architecture

```text
USER PROFILE
      ↓

┌──────────────────────────────────────┐
│ Candidate Information                │
│                                      │
│ - Technical Skills                   │
│ - Soft Skills                        │
│ - Preferred Career Roles             │
│ - Experience                         │
│ - Education                          │
│ - English Level                      │
│ - Danish Level                       │
│ - Preferred Locations                │
│ - Preferred Work Modes               │
│ - Preferred Employment Types         │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Build User Profile                   │
│                                      │
│ technical_skills +                   │
│ soft_skills +                        │
│ preferred_roles                      │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Build Job Profiles                   │
│                                      │
│ technical_skills_required +          │
│ soft_skills_required +               │
│ role_category                        │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ TF-IDF Vectorization                 │
│                                      │
│ Convert text profiles into vectors   │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Cosine Similarity                    │
│                                      │
│ Measures semantic similarity         │
│ between user profile and jobs        │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Exact Skill Matching                 │
│                                      │
│ - Technical Skill Overlap            │
│ - Soft Skill Overlap                 │
│ - Missing Skills Detection           │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Structured Matching                  │
│                                      │
│ - Experience Match                   │
│ - Education Match                    │
│ - English Match                      │
│ - Danish Match                       │
│ - Location Match                     │
│ - Work Mode Match                    │
│ - Employment Type Match              │
└──────────────────────────────────────┘
      ↓

┌──────────────────────────────────────┐
│ Hybrid Final Scoring Engine          │
│                                      │
│ Combines all scores into             │
│ a final recommendation score         │
└──────────────────────────────────────┘
      ↓

FINAL CAREER RECOMMENDATIONS
```

---

# ⚙️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn

---

# 🔍 Core Recommendation Logic

The system uses a hybrid recommendation approach.

## 1. Semantic Similarity

Uses:
- TF-IDF Vectorization
- Cosine Similarity

to measure semantic similarity between:
- user profile
- job profile

This helps the system understand contextual relevance and profile similarity.

---

## 2. Exact Skill Matching

Uses set intersection to calculate:
- matched technical skills
- missing technical skills
- matched soft skills
- missing soft skills

This layer improves:
- explainability
- transparency
- skill gap analysis

---

## 3. Structured Matching

Calculates additional scores for:
- experience level
- education level
- English language level
- Danish language level
- preferred locations
- preferred work modes
- preferred employment types

This layer applies business rules and user preferences.

---

# 📊 Final Recommendation Formula

```python
final_score = (

    similarity_score * 0.35 +

    technical_score * 0.20 +

    soft_score * 0.10 +

    exp_score * 0.10 +

    education_score * 0.08 +

    english_score * 0.05 +

    danish_score * 0.05 +

    location_score * 0.03 +

    work_mode_score * 0.02 +

    employment_score * 0.02
)
```

---

# ✨ Key Features

- Hybrid recommendation engine
- Explainable AI recommendations
- Semantic career matching
- Exact skill matching
- Skill gap analysis
- Personalized success roadmap
- Interactive visual analytics
- Career readiness scoring
- Market-driven skill prioritization
- Decision-support dashboard

---

# 📈 Decision-Support Visual Analytics

The dashboard includes:

- Radar Charts
- Gauge Charts
- Donut Charts
- Match Category Analysis
- Missing Skill Prioritization
- Career Readiness Visualization
- Market-Driven Skill Gap Analysis

These visualizations help users understand:
- career strengths
- hiring weaknesses
- market readiness
- improvement priorities
- high-impact missing skills

---

# 📂 Project Structure

```text
career_recommendation_system/

│
├── data/
│
│   ├── cleaned_jobs_dataset.csv
│   │   → Main cleaned jobs dataset used for recommendations
│   │
│   ├── technical_skills.csv
│   │   → Technical skills reference dataset
│   │
│   ├── soft_skills.csv
│   │   → Soft skills reference dataset
│   │
│   ├── tech_skills_by_role.csv
│   │   → Technical skill frequency by role category
│   │
│   └── soft_skills_by_role.csv
│       → Soft skill frequency by role category
│
│
├── scripts/
│
│   ├── app.py
│   │   → Main Streamlit application entry point
│   │
│   ├── config.py
│   │   → Global configuration, thresholds, weights, and constants
│   │
│   ├── matching_engine.py
│   │   → Hybrid recommendation and scoring engine
│   │
│   ├── styles.py
│   │   → Custom CSS styling and dashboard appearance
│   │
│   └── ui/
│
│       ├── __init__.py
│       │   → Centralized UI component imports
│       │
│       ├── header.py
│       │   → Main dashboard hero/header section
│       │
│       ├── candidate_form.py
│       │   → Candidate profile input form
│       │
│       ├── user_profile_summary.py
│       │   → Candidate profile summary section
│       │
│       ├── match_analysis.py
│       │   → Match score analysis and recommendation breakdown
│       │
│       ├── skill_gap_analysis.py
│       │   → Skill matching and gap analysis
│       │
│       ├── success_roadmap.py
│       │   → Personalized career improvement roadmap
│       │
│       ├── visualizations.py
│       │   → Interactive charts and decision-support analytics
│       │
│       └── job_components.py
│           → Reusable job recommendation UI components
│
│
├── README.md
│   → Project documentation
│
└── requirements.txt
    → Python dependencies
```

---

# 🧠 Architecture Design

The project follows a modular architecture.

## Business Logic Layer

Handles:
- recommendation generation
- similarity calculations
- scoring logic
- skill matching
- ranking logic

Main file:
```text
matching_engine.py
```

---

## UI Layer

Handles:
- rendering
- layout
- dashboard sections
- visual analytics
- decision-support insights

Main folder:
```text
ui/
```

---

## Configuration Layer

Handles:
- thresholds
- scoring weights
- constants

Main file:
```text
config.py
```

---

## Data Layer

Handles:
- cleaned datasets
- market skill analysis
- role-based skill frequencies

Main folder:
```text
data/
```

---

# 🚀 How To Run

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the application

```bash
streamlit run scripts/app.py
```

---

