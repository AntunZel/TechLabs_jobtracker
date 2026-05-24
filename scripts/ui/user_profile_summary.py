import streamlit as st


# ============================================================
# PROFILE SUMMARY
# ============================================================

def render_profile_summary(candidate_data):

    preferred_roles_text = (
        ", ".join(candidate_data["preferred_roles"])
        if candidate_data["preferred_roles"]
        else "multiple career opportunities"
    )

    technical_skills_text = (
        ", ".join(candidate_data["technical_skills"])
        if candidate_data["technical_skills"]
        else "No technical skills selected"
    )

    soft_skills_text = (
        ", ".join(candidate_data["soft_skills"])
        if candidate_data["soft_skills"]
        else "No soft skills selected"
    )

    display_locations = (

        "All Locations"

        if "All" in candidate_data["preferred_locations"]

        else ", ".join(candidate_data["preferred_locations"])
    )

    display_work_modes = (

        "All (Remote, Hybrid, On-site)"

        if "All" in candidate_data["preferred_work_modes"]

        else ", ".join(candidate_data["preferred_work_modes"])
    )

    display_employment_types = (

        "All (Full-time, Part-time, Internship)"

        if "All" in candidate_data["preferred_employment_types"]

        else ", ".join(candidate_data["preferred_employment_types"])
    )

    summary_html = f"""

    <div style="
    background:white;
    padding:40px;
    border-radius:28px;
    box-shadow:0 8px 24px rgba(0,0,0,0.06);
    line-height:2.1;
    font-size:19px;
    color:#374151;
    margin-bottom:35px;
    ">

    <div style="
    font-size:34px;
    font-weight:900;
    color:#111827;
    margin-bottom:28px;
    ">

    Your Professional Profile Summary

    </div>

    <p>

    You are a candidate with a
    <b>{candidate_data["education"]}</b>
    and approximately
    <b>{candidate_data["experience"]} years</b>
    of professional experience.

    </p>

    <p>

    Your primary career focus is currently on
    <b>{preferred_roles_text}</b>
    opportunities.

    </p>

    <p>

    You prefer working in
    <b>{display_locations}</b>
    with a
    <b>{display_work_modes}</b>
    work setup and
    <b>{display_employment_types}</b>
    employment type.

    </p>

    <p>

    Your technical skill set includes
    <b>{technical_skills_text}</b>.

    </p>

    <p>

    On the soft skills side, you are confident in
    <b>{soft_skills_text}</b>.

    </p>

    <p>

    Your English level is
    <b>{candidate_data["english_level"]}</b>
    and your Danish level is
    <b>{candidate_data["danish_level"]}</b>.

    </p>

    <p>

    You are looking for opportunities where you can continue growing,
    contribute to impactful projects, and help drive real business value.

    </p>

    </div>
    """

    st.markdown(summary_html, unsafe_allow_html=True)



