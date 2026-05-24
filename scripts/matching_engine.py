# ============================================================
# IMPORTS
# ============================================================

import pandas as pd

from config import (
    SIMILARITY_WEIGHT,
    TECHNICAL_SKILL_WEIGHT,
    SOFT_SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT,
    ENGLISH_WEIGHT,
    DANISH_WEIGHT,
    LOCATION_WEIGHT,
    WORK_MODE_WEIGHT,
    EMPLOYMENT_WEIGHT
)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def split_skills(value):

    if pd.isna(value) or value == "":
        return set()

    return set([
        skill.strip().lower()
        for skill in str(value).split(",")
        if skill.strip()
    ])

# ============================================================
# MATCH  FUNCTIONS
# ============================================================

# -------------------------------------------------
# skill match: Technical and Soft Skills
# -------------------------------------------------

def calculate_skill_match(user_skills, required_skills):

    user_set = set([
        skill.lower()
        for skill in user_skills
    ])

    required_set = split_skills(required_skills)

    if len(required_set) == 0:
        return 1, set(), set()

    matched = user_set.intersection(required_set)

    missing = required_set.difference(user_set)

    score = len(matched) / len(required_set)

    return score, matched, missing


# -------------------------------------------------
# experience_match
# -------------------------------------------------

def experience_match(user_exp, required_exp):

    try:
        required_exp = float(required_exp)

    except ValueError:
        required_exp = 0

    if required_exp == 0:
        return 1

    if user_exp >= required_exp:
        return 1

    return user_exp / required_exp


# -------------------------------------------------
# education_match
# -------------------------------------------------

def education_match(user_education, job_education):

    education_levels = {

        "bachelor's degree": 1,

        "master's degree": 2,

        "phd": 3
    }

    user_score = education_levels.get(
        str(user_education).strip().lower(),
        0
    )

    job_score = education_levels.get(
        str(job_education).strip().lower(),
        0
    )

    if job_score == 0:
        return 1

    if user_score >= job_score:
        return 1

    return user_score / job_score

# -------------------------------------------------
# language_match  Danish and English Language
# -------------------------------------------------

def language_match(user_level, job_level, language="english"):

    level_maps = {

        "english": {
            "intermediate": 1,
            "advanced": 2,
            "fluent": 3
        },

        "danish": {
            "basic": 1,
            "intermediate": 2
        }
    }

    levels = level_maps.get(language, {})

    user_score = levels.get(
        str(user_level).strip().lower(),
        0
    )

    job_score = levels.get(
        str(job_level).strip().lower(),
        0
    )

    if job_score == 0:
        return 1

    if user_score >= job_score:
        return 1

    return user_score / job_score


# -------------------------------------------------
# location / work_mode / employment_type match
# -------------------------------------------------

def preference_match(user_values, job_value):

    job_value = str(job_value).strip().lower()

    user_values = [

        str(value).strip().lower()

        for value in user_values
    ]

    if "all" in user_values:
        return 1

    if job_value in user_values:
        return 1

    return 0

# ============================================================
# SIMILARITY
# ============================================================

def generate_similarity_scores(filtered_jobs_df, user_profile):

    tfidf = TfidfVectorizer()

    job_vectors = tfidf.fit_transform(filtered_jobs_df["job_profile"])

    user_vector = tfidf.transform([user_profile])

    similarity_scores = cosine_similarity(user_vector,job_vectors).flatten()

    return similarity_scores

# ============================================================
# SCORE CALCULATION
# ============================================================

def calculate_job_match_scores(job, candidate_data, similarity_score):

    technical_score, matched_tech, missing_tech = (
        calculate_skill_match(
            candidate_data["technical_skills"],
            job["technical_skills_required"]
        )
    )

    soft_score, matched_soft, missing_soft = (
        calculate_skill_match(
            candidate_data["soft_skills"],
            job["soft_skills_required"]
        )
    )

    exp_score = experience_match(
        candidate_data["experience"],
        job["experience_required_years"]
    )

    location_score = preference_match(
        candidate_data["preferred_locations"],
        job["city"]
    )

    work_mode_score = preference_match(
        candidate_data["preferred_work_modes"],
        job["work_mode"]
    )

    employment_score = preference_match(
        candidate_data["preferred_employment_types"],
        job["employment_type"]
    )

    education_score = education_match(
        candidate_data["education"],
        job["education_required"]
    )

    english_score = language_match(
        candidate_data["english_level"],
        job["English_required_level"],
        language="english"
    )

    danish_score = language_match(
        candidate_data["danish_level"],
        job["Danish_required_level"],
        language="danish"
    )

    return {

        "similarity_score": similarity_score,

        "technical_score": technical_score,

        "soft_score": soft_score,

        "exp_score": exp_score,

        "location_score": location_score,

        "work_mode_score": work_mode_score,

        "employment_score": employment_score,

        "education_score": education_score,

        "english_score": english_score,

        "danish_score": danish_score,

        "matched_tech": matched_tech,

        "missing_tech": missing_tech,

        "matched_soft": matched_soft,

        "missing_soft": missing_soft
    }


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(scores):

    final_score = (

        scores["similarity_score"] * SIMILARITY_WEIGHT +

        scores["technical_score"] * TECHNICAL_SKILL_WEIGHT +

        scores["soft_score"] * SOFT_SKILL_WEIGHT +

        scores["exp_score"] * EXPERIENCE_WEIGHT +

        scores["education_score"] * EDUCATION_WEIGHT +

        scores["english_score"] * ENGLISH_WEIGHT +

        scores["danish_score"] * DANISH_WEIGHT +

        scores["location_score"] * LOCATION_WEIGHT +

        scores["work_mode_score"] * WORK_MODE_WEIGHT +

        scores["employment_score"] * EMPLOYMENT_WEIGHT
    )

    return final_score


# ============================================================
# RESULT BUILDER
# ============================================================

def build_recommendation_result(job, scores, final_score):

    return {

        "Company":
            job["company_name"],

        "Job Title":
            job["job_title"],

        "Role Category":
            job["role_category"],

        "City":
            job["city"],

        "Work Mode":
            job["work_mode"],

        "Employment Type":
            job["employment_type"],

        "Final Match Score":
            round(final_score * 100, 2),

        "Technical Match":
            round(scores["technical_score"] * 100, 2),

        "Soft Skill Match":
            round(scores["soft_score"] * 100, 2),

        "Experience Match":
            round(scores["exp_score"] * 100, 2),

        "Education Match":
            round(scores["education_score"] * 100, 2),

        "English Match":
            round(scores["english_score"] * 100, 2),

        "Danish Match":
            round(scores["danish_score"] * 100, 2),

        "Location Match":
            round(scores["location_score"] * 100, 2),

        "Work Mode Match":
            round(scores["work_mode_score"] * 100, 2),

        "Employment Match":
            round(scores["employment_score"] * 100, 2),

        "Semantic Similarity":
            round(scores["similarity_score"] * 100, 2),

        "Matched Technical":
            sorted(scores["matched_tech"]),

        "Missing Technical":
            sorted(scores["missing_tech"]),

        "Matched Soft":
            sorted(scores["matched_soft"]),

        "Missing Soft":
            sorted(scores["missing_soft"])
    }

# ============================================================
# MAIN ENGINE FLOW
# ============================================================

# generate_recommendations()
#
# 1. Build job profile
# 2. Build user profile
# 3. Generate semantic similarity scores
# 4. Calculate job match scores
# 5. Calculate final weighted score
# 6. Build recommendation result dictionary
# 7. Create recommendations DataFrame
# 8. Sort recommendations by final score
# 9. Return recommendations DataFrame


def generate_recommendations(candidate_data, filtered_jobs_df):

    filtered_jobs_df = filtered_jobs_df.copy()

    # BUILD JOB PROFILE
    filtered_jobs_df["job_profile"] = (

        filtered_jobs_df["technical_skills_required"].astype(str)

        + " " +

        filtered_jobs_df["soft_skills_required"].astype(str)

        + " " +

        filtered_jobs_df["role_category"].astype(str)

    ).str.lower()

    # BUILD USER PROFILE
    user_profile = " ".join(

        candidate_data["technical_skills"]

        +

        candidate_data["soft_skills"]

        +

        candidate_data["preferred_roles"]

    ).lower()

    # GENERATE SIMILARITY SCORES
    similarity_scores = generate_similarity_scores(

        filtered_jobs_df,

        user_profile
    )

    # MATCH CALCULATION
    results = []

    for idx, (_, job) in enumerate(

        filtered_jobs_df.iterrows()
    ):

        similarity_score = similarity_scores[idx]

        # MATCH SCORES
        scores = calculate_job_match_scores(

            job,

            candidate_data,

            similarity_score
        )

        # FINAL SCORE
        final_score = calculate_final_score(scores)


        # BUILD RECOMMENDATION RESULT
        recommendation = build_recommendation_result(job, scores, final_score)

        results.append(recommendation)

    # DATAFRAME CREATION
    recommendations_df = pd.DataFrame(results)

    # SORTING
    recommendations_df = recommendations_df.sort_values(by="Final Match Score", ascending=False).reset_index(drop=True)
    
    # RETURN
    return recommendations_df

