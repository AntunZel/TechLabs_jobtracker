import streamlit as st


# ============================================================
# ATS RANK BADGE
# ============================================================

def render_rank_badge(index):

    st.markdown(f"""
    <div class="rank-badge">

    ATS Rank #{index + 1}

    </div>
    """, unsafe_allow_html=True)

# ============================================================
# JOB HEADER
# ============================================================

def render_job_header(row):

    st.markdown(f"""
    <div class="job-title">

    {row['Job Title']}

    </div>
    """, unsafe_allow_html=True)


    st.caption(

        f"{row['Company']} • "

        f"{row['City']} • "

        f"{row['Work Mode']} • "

        f"{row['Employment Type']}"
    )

