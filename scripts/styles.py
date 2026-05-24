
import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* =========================================================
       GLOBAL BACKGROUND (YOUR ORIGINAL)
    ========================================================= */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background-color:#F5EDED;
    }

    html,
    body,
    .stApp {
        font-family:'Segoe UI', sans-serif;
        color:#111827;
    }


    /* =========================================================
       TYPOGRAPHY (YOUR ORIGINAL)
    ========================================================= */

    .section-title {
        font-size:30px;
        font-weight:700;
        margin-top:25px;
        margin-bottom:25px;
        color:#0f172a;
    }

    .sub-section-title {
        font-size:22px;
        font-weight:500;
        color:#111827;
        margin-top:22px;
        margin-bottom:18px;
        line-height:1.4;
    }

    .job-title {
        font-size:40px;
        font-weight:900;
        color:#0f172a;
        margin-bottom:6px;
    }

    .content-title {
        font-size:18px;
        font-weight:700;
        color:#111827;
        margin-top:18px;
        margin-bottom:14px;
        margin-left:14px;
        line-height:1.4;
    }


    /* =========================================================
       SKILLS CONTAINER (YOUR ORIGINAL)
    ========================================================= */

    .skills-container {
        display:flex;
        flex-wrap:wrap;
        gap:12px;
        margin-top:10px;
        margin-bottom:20px;
    }


    /* =========================================================
       RANK BADGE (YOUR ORIGINAL)
    ========================================================= */

    .rank-badge {
        display:inline-block;
        background:linear-gradient(135deg,#2563eb,#1d4ed8);
        color:white;
        padding:10px 18px;
        border-radius:12px;
        font-weight:700;
        margin-bottom:18px;
        box-shadow:0 4px 14px rgba(37,99,235,0.18);
    }


    /* =========================================================
       SKILL PILLS (YOUR ORIGINAL)
    ========================================================= */

    .skill-pill-green {
        display:inline-flex;
        align-items:center;
        justify-content:center;
        vertical-align:middle;
        background:#dcfce7;
        color:#166534;
        padding:10px 16px;
        border-radius:20px;
        font-size:14px;
        font-weight:700;
        margin:6px;
        min-height:44px;
        border:1px solid #bbf7d0;
    }

    .skill-pill-red {
        display:inline-flex;
        align-items:center;
        justify-content:center;
        vertical-align:middle;
        background:#fee2e2;
        color:#991b1b;
        padding:10px 16px;
        border-radius:20px;
        font-size:14px;
        font-weight:700;
        margin:6px;
        min-height:44px;
        border:1px solid #fecaca;
    }


    /* =========================================================
       COLUMN STRETCH (YOUR ORIGINAL)
    ========================================================= */

    div[data-testid="column"] {
        align-self:stretch !important;
    }


    /* =========================================================
       =============== NEW ADDITIONS FOR VISUALIZATIONS ===============
    ========================================================= */


    /* =========================================================
       KPI CARDS (NEW - for metric display)
    ========================================================= */

    .kpi-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }


    /* =========================================================
       INSIGHT BOX (NEW - for executive insights)
    ========================================================= */

    .insight-box {
        background: linear-gradient(135deg, rgba(239,68,68,0.05), rgba(245,158,11,0.05));
        border: 1px solid rgba(239,68,68,0.12);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
    }


    /* =========================================================
       RECOMMENDATION CARD (NEW - for action items)
    ========================================================= */

    .recommendation-card {
        background: white;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }

    .recommendation-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: rgba(37,99,235,0.2);
    }


    /* =========================================================
       PLOTLY CHART CONTAINERS (NEW)
    ========================================================= */

    div[data-testid="stPlotlyChart"] {
        background: white;
        border-radius: 20px;
        padding: 16px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }

    div[data-testid="stPlotlyChart"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }


    /* =========================================================
       METRIC STYLES (NEW - for st.metric)
    ========================================================= */

    div[data-testid="stMetricLabel"] {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.3px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 42px;
        font-weight: 800;
        color: #0F172A;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 20px;
        background: #F1F5F9;
        display: inline-block;
    }


    /* =========================================================
       CAPTION STYLES (NEW - for chart insights)
    ========================================================= */

    .stCaption {
        font-size: 12px;
        color: #64748B;
        margin-top: 8px;
        text-align: center;
    }


    /* =========================================================
       DIVIDER STYLES (NEW)
    ========================================================= */

    hr {
        margin: 24px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    }

    </style>
    """, unsafe_allow_html=True)