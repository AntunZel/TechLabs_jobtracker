import streamlit as st

# ============================================================
# HEADER
# ============================================================

def render_header():

    st.markdown("""
    <div style="
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding:14px 32px;
    border-radius:24px;
    text-align:center;
    margin-bottom:28px;
    box-shadow:0 6px 20px rgba(0,0,0,0.10);
    ">

    <div style="
    font-size:36px;
    margin-bottom:0px;
    ">
    🚀
    </div>

    <div style="
    font-size:42px;
    font-weight:900;
    color:white;
    line-height:1.05;
    margin-bottom:10px;
    ">

    Career Recommendation System

    </div>

    <div style="
    font-size:18px;
    color:#cbd5e1;
    max-width:850px;
    margin:auto;
    line-height:1.5;
    font-weight:400;
    ">

    Analyze your profile and discover the best matching career opportunities
    based on your skills, experience, qualifications and career preferences.

    </div>

    </div>
    """, unsafe_allow_html=True)
