# ============================================================
# IMPORTS
# ============================================================

import pandas as pd
import streamlit as st

from styles import load_css

from matching_engine import generate_recommendations


from ui import (
    render_header,
    render_candidate_form,
    render_profile_summary,
    render_match_analysis,
    render_skill_gap_analysis,
    render_success_roadmap,
    render_visualizations,
    render_rank_badge,
    render_job_header
)



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Career Recommendation System",

    layout="wide"
)

# ============================================================
# LOAD CSS
# ============================================================

load_css()

# ============================================================
# HEADER
# ============================================================

render_header()

# ============================================================
# LOAD DATA
# ============================================================

jobs_df = pd.read_csv("../data/cleaned_jobs_dataset.csv")

tech_df = pd.read_csv("../data/technical_skills.csv")

soft_df = pd.read_csv("../data/soft_skills.csv")

jobs_df = jobs_df.fillna("")

# ============================================================
# FORM SECTION
# ============================================================

technical_skills_list = (

    tech_df["skill"]

    .dropna()

    .astype(str)

    .str.lower()

    .str.strip()

    .unique()

    .tolist()
)


soft_skills_list = (

    soft_df["skill"]

    .dropna()

    .astype(str)

    .str.lower()

    .str.strip()

    .unique()

    .tolist()
)

form_data = render_candidate_form(jobs_df, technical_skills_list, soft_skills_list)

if form_data["submitted"]:

    candidate_data = form_data

    # VALIDATION
    if not candidate_data["technical_skills"]:

        st.warning(
            "⚠️ Please select at least one technical skill."
        )

        st.stop()


    if not candidate_data["soft_skills"]:

        st.warning(
            "⚠️ Please select at least one soft skill."
        )

        st.stop()

    if not candidate_data["preferred_roles"]:

        st.warning(
            "⚠️ Please select at least one preferred career role."
        )

        st.stop()

    # FILTER JOBS
    filtered_jobs_df = jobs_df.copy()
    
    if filtered_jobs_df.empty:

        st.warning(

            "⚠️ No matching jobs found for selected career roles."
        )

        st.stop()

    if candidate_data["preferred_roles"]:

        filtered_jobs_df = filtered_jobs_df[filtered_jobs_df["role_category"].isin(candidate_data["preferred_roles"])]

    # GENERATE RECOMMENDATIONS
    recommendations_df = generate_recommendations(

        candidate_data,

        filtered_jobs_df
    )

    # PROFILE SUMMARY
    render_profile_summary(candidate_data)

    # TOP JOBS
    top_jobs = recommendations_df.head(5)

    # JOB DETAILS
    for index, row in top_jobs.iterrows():

        render_rank_badge(index)

        with st.expander(

            f"🥇 • {row['Job Title']} • {row['Final Match Score']}%",

            expanded=(index == 0)
        ):

            render_job_header(row)

            render_match_analysis(row)

            render_skill_gap_analysis(row, candidate_data)

            render_success_roadmap(row)

            render_visualizations(row, candidate_data)
