import streamlit as st


# ============================================================
# CANDIDATE FORM
# ============================================================

def render_candidate_form(jobs_df, technical_skills_list, soft_skills_list):

    with st.form("candidate_form"):

        st.header("👤 Candidate Profile")

        # ----------------------------------------------------
        # TECHNICAL SKILLS
        # ----------------------------------------------------

        technical_skills = st.multiselect(

            "Technical Skills",

            technical_skills_list,

            placeholder="Select technical skills"
        )

        # ----------------------------------------------------
        # SOFT SKILLS
        # ----------------------------------------------------

        soft_skills = st.multiselect(

            "Soft Skills",

            soft_skills_list,

            placeholder="Select soft skills"
        )

        # ----------------------------------------------------
        # ROLE CATEGORY
        # ----------------------------------------------------

        role_categories = (

            jobs_df["role_category"]

            .dropna()

            .astype(str)

            .str.strip()

            .unique()

            .tolist()
        )

        role_categories = sorted(role_categories)

        preferred_roles = st.multiselect(

            "Preferred Career Roles",

            role_categories,

            placeholder="Select preferred career roles"
        )

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        experience = st.slider("Years of Experience", 0, 15, 2)

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        education = st.selectbox(

            "Education Level",

            [
                "Bachelor's Degree",

                "Master's Degree",

                "PhD"
            ]
        )

        # ----------------------------------------------------
        # ENGLISH LEVEL
        # ----------------------------------------------------

        english_level = st.selectbox(

            "English Level",

            [
                "Intermediate",

                "Advanced",

                "Fluent"
            ]
        )

        # ----------------------------------------------------
        # DANISH LEVEL
        # ----------------------------------------------------

        danish_level = st.selectbox(

            "Danish Level",

            [
                "Basic",

                "Intermediate"
            ]
        )

        # ----------------------------------------------------
        # LOCATIONS
        # ----------------------------------------------------

        cities = (

            jobs_df["city"]

            .dropna()

            .astype(str)

            .str.strip()

            .unique()

            .tolist()
        )

        cities = sorted(cities)

        preferred_locations = st.multiselect(

            "Preferred Locations",

            options=["All"] + cities,

            default=["All"]
        )

        if (
            "All" in preferred_locations

            and len(preferred_locations) > 1
        ):

            preferred_locations = ["All"]

        # ----------------------------------------------------
        # WORK MODES
        # ----------------------------------------------------

        preferred_work_modes = st.multiselect(

            "Preferred Work Modes",

            options=[
                "All",
                "Remote",
                "Hybrid",
                "On-site"
            ],

            default=["All"]
        )

        if (
            "All" in preferred_work_modes

            and len(preferred_work_modes) > 1
        ):

            preferred_work_modes = ["All"]

        # ----------------------------------------------------
        # EMPLOYMENT TYPES
        # ----------------------------------------------------

        preferred_employment_types = st.multiselect(

            "Preferred Employment Types",

            options=[
                "All",
                "Full-time",
                "Part-time",
                "Internship"
            ],

            default=["All"]
        )

        if (
            "All" in preferred_employment_types

            and len(preferred_employment_types) > 1
        ):

            preferred_employment_types = ["All"]

        # ----------------------------------------------------
        # SUBMIT BUTTON
        # ----------------------------------------------------

        submitted = st.form_submit_button(

            "🚀 Analyze My Profile",

            use_container_width=True
        )

    return {

        "submitted": submitted,

        "technical_skills": technical_skills,

        "soft_skills": soft_skills,

        "preferred_roles": preferred_roles,

        "experience": experience,

        "education": education,

        "english_level": english_level,

        "danish_level": danish_level,

        "preferred_locations": preferred_locations,

        "preferred_work_modes": preferred_work_modes,

        "preferred_employment_types": preferred_employment_types
    }
