# ============================================================
# visualizations.py 
# Executive Career Intelligence Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import uuid

from typing import Tuple, Dict, Any, List

# ============================================================
# COLORS
# ============================================================

PRIMARY = "#2563EB"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
PURPLE = "#8B5CF6"


# ============================================================
# LOAD DATASETS
# ============================================================

@st.cache_data
def load_technical_skills() -> pd.DataFrame:
    return pd.read_csv("../data/tech_skills_by_role.csv")

@st.cache_data
def load_soft_skills() -> pd.DataFrame:
    return pd.read_csv("../data/soft_skills_by_role.csv")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_missing_skills_priority(
    row: pd.Series,
    candidate_data: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    selected_roles = candidate_data.get("preferred_roles", [])

    if not selected_roles:
        return pd.DataFrame(), pd.DataFrame()

    tech_df = load_technical_skills()
    technical_role_df = tech_df[tech_df["role_category"].isin(selected_roles)]

    if not technical_role_df.empty:
        technical_priority_df = (
            technical_role_df
            .groupby("skill")["technical_skills_required"]
            .sum()
            .reset_index()
        )
        total = technical_priority_df["technical_skills_required"].sum()
        if total > 0:
            technical_priority_df["importance_percent"] = technical_priority_df["technical_skills_required"] / total * 100
        else:
            technical_priority_df["importance_percent"] = 0

        missing_technical = [s.lower() for s in row.get("Missing Technical", [])]
        technical_priority_df = (
            technical_priority_df[technical_priority_df["skill"].str.lower().isin(missing_technical)]
            .sort_values("importance_percent", ascending=False)
            .head(5)
        )
    else:
        technical_priority_df = pd.DataFrame()

    soft_df = load_soft_skills()
    soft_role_df = soft_df[soft_df["role_category"].isin(selected_roles)]

    if not soft_role_df.empty:
        soft_priority_df = (
            soft_role_df
            .groupby("skill")["soft_skills_required"]
            .sum()
            .reset_index()
        )
        total = soft_priority_df["soft_skills_required"].sum()
        if total > 0:
            soft_priority_df["importance_percent"] = soft_priority_df["soft_skills_required"] / total * 100
        else:
            soft_priority_df["importance_percent"] = 0

        missing_soft = [s.lower() for s in row.get("Missing Soft", [])]
        soft_priority_df = (
            soft_priority_df[soft_priority_df["skill"].str.lower().isin(missing_soft)]
            .sort_values("importance_percent", ascending=False)
            .head(5)
        )
    else:
        soft_priority_df = pd.DataFrame()

    return technical_priority_df, soft_priority_df


# ============================================================
# GAUGE CHART
# ============================================================

def create_gauge_chart(score: float) -> go.Figure:

    if score < 40:
        main_color = "#DC2626"
        status = "Critical"
    elif score < 70:
        main_color = "#D97706"
        status = "Moderate"
    else:
        main_color = "#059669"
        status = "Strong"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0.06, 0.96], 'y': [0, 1]},
        number={
            "suffix": "%",
            "font": {"size": 48, "color": main_color, "family": "Arial Black"}
        },
        title={"text": f"<b>{status}</b>", "font": {"size": 18, "color": main_color}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickvals": [0, 20, 40, 60, 80, 100],
                "ticktext": ["0", "20", "40", "60", "80", "100"],
                "tickwidth": 3,
                "tickcolor": "#475569",
                "tickfont": {"size": 13, "color": "#334155"}
            },
            "bar": {"color": "#0F172A", "thickness": 0.16},
            "steps": [
                {"range": [0, 40], "color": "#F87171"},
                {"range": [40, 70], "color": "#F59E0B"},
                {"range": [70, 100], "color": "#34D399"}
            ],
            "threshold": {
                "line": {"color": main_color, "width": 7},
                "thickness": 0.9,
                "value": score
            },
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0
        }
    ))

    fig.update_layout(
        height=400,
        margin=dict(t=60, b=80, l=55, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Arial", "color": "#0F172A"}
    )
    
    fig.add_annotation(
        x=0.5, y=1.18, xref="paper", yref="paper",
        text="<b>Overall Candidate Readiness Score</b>",
        showarrow=False, font=dict(size=16, color="#0F172A")
    )
    
    fig.add_annotation(
        x=0.5, y=-0.12, xref="paper", yref="paper",
        text="<span style='color:#DC2626;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Critical (0-40)</span>  "
             "<span style='color:#D97706;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Moderate (40-70)</span>  "
             "<span style='color:#059669;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Strong (70-100)</span>",
        showarrow=False, font=dict(size=13, weight="bold"), align="center"
    )

    return fig


# ============================================================
# RADAR CHART
# ============================================================

def create_radar_chart(scores: Dict[str, float]) -> go.Figure:

    categories = list(scores.keys())
    values = list(scores.values())

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(37,99,235,0.15)',
            line=dict(color=PRIMARY, width=2.5),
            name="Your Profile"
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[100] * len(categories),
            theta=categories,
            fill=None,
            line=dict(color='#94A3B8', width=1.5, dash='dash'),
            name="Target (100%)"
        )
    )

    fig.update_layout(
        height=400,
        margin=dict(t=60, b=80, l=60, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color='#64748B'),
                tickvals=[20, 40, 60, 80, 100],
                ticktext=['20%', '40%', '60%', '80%', '100%'],
                gridcolor='#E2E8F0',
                gridwidth=0.5
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color='#334155'),
                gridcolor='#E2E8F0',
                gridwidth=0.5,
                rotation=90,
                direction='clockwise'
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=13, color="#334155", weight="bold"),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E2E8F0',
            borderwidth=1
        )
    )

    fig.add_annotation(
        x=0.5, y=1.18,
        xref="paper", yref="paper",
        text="<b>Candidate Match Radar</b>",
        showarrow=False,
        font=dict(size=16, color="#0F172A")
    )

    return fig


# ============================================================
# DONUT CHART
# ============================================================

def create_donut_chart(
    tech_matched: int, 
    tech_missing: int, 
    soft_matched: int, 
    soft_missing: int
) -> go.Figure:
    
    tech_total = tech_matched + tech_missing
    soft_total = soft_matched + soft_missing
    total = tech_total + soft_total
    
    labels = ['Technical Skills - Matched', 'Technical Skills - Missing', 'Soft Skills - Matched', 'Soft Skills - Missing']
    values = [tech_matched, tech_missing, soft_matched, soft_missing]
    colors = [SUCCESS, '#EF4444', '#A855F7', '#F97316']
    
    hover_texts = [
        f'Technical Skills<br>Matched: {tech_matched} skills',
        f'Technical Skills<br>Missing: {tech_missing} skills',
        f'Soft Skills<br>Matched: {soft_matched} skills',
        f'Soft Skills<br>Missing: {soft_missing} skills'
    ]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hole=0.65,
        textinfo='percent',
        textposition='inside',
        textfont=dict(size=11, color='white', weight='bold'),
        hovertext=hover_texts,
        hoverinfo='text+percent',
        showlegend=False
    )])
    
    fig.update_layout(
        height=400,
        margin=dict(t=60, b=80, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(text=f"<b>{total}</b>", x=0.5, y=0.5, font=dict(size=20, color="#0F172A", weight="bold"), showarrow=False),
            dict(text="Total Skills", x=0.5, y=0.44, font=dict(size=10, color="#64748B"), showarrow=False),
            dict(text=f"✓ Matched: {tech_matched + soft_matched}<br>✗ Missing: {tech_missing + soft_missing}", x=0.5, y=0.34, font=dict(size=9, color="#64748B"), showarrow=False)
        ]
    )
    
    fig.add_annotation(
        x=0.5, y=1.12, xref="paper", yref="paper",
        text="<b>Candidate Skills Distribution</b>",
        showarrow=False, font=dict(size=16, color="#0F172A")
    )
    
    fig.add_annotation(
        x=0.5, y=-0.12, xref="paper", yref="paper",
        text="<span style='color:#10B981;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Matched</span>  "
             "<span style='color:#EF4444;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Missing</span>  "
             "<span style='color:#A855F7;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Soft Skills</span>  "
             "<span style='color:#F97316;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Soft Missing</span>",
        showarrow=False, font=dict(size=13, weight="bold"), align="center"
    )

    return fig


# ============================================================
# CATEGORY BAR CHART
# ============================================================

def create_category_bar_chart(scores: Dict[str, float]) -> go.Figure:
    df = pd.DataFrame([{"Category": k, "Score": v} for k, v in scores.items()])
    df = df.sort_values("Score", ascending=True)
    
    colors = []
    for score in df["Score"]:
        if score < 40:
            colors.append("#EF4444")
        elif score < 70:
            colors.append("#F59E0B")
        else:
            colors.append("#10B981")
    
    fig = go.Figure(go.Bar(
        x=df["Score"],
        y=df["Category"],
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=1), cornerradius=5),
        text=df["Score"].apply(lambda x: f"{x:.0f}%"),
        textposition='outside',
        textfont=dict(size=11, weight='bold', color='#1E293B'),
        hovertemplate='%{y}: %{x:.0f}%<extra></extra>',
        width=0.7
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(t=60, b=80, l=110, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title="", 
            range=[0, 105], 
            gridcolor="#E2E8F0", 
            showticklabels=False,
            showline=False,
            zeroline=False
        ),
        yaxis=dict(title="", tickfont=dict(size=11, color="#334155", weight='bold')),
        showlegend=False
    )
    
    fig.add_annotation(
        x=0.5, y=1.12, xref="paper", yref="paper",
        text="<b>Match Category Scores</b>",
        showarrow=False, font=dict(size=16, color="#0F172A")
    )
    
    fig.add_annotation(
        x=0.5, y=-0.12, xref="paper", yref="paper",
        text="<span style='color:#EF4444;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Critical (0-40)</span>  "
             "<span style='color:#F59E0B;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Moderate (40-70)</span>  "
             "<span style='color:#10B981;font-size:13px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>Strong (70-100)</span>",
        showarrow=False, font=dict(size=13, weight="bold"), align="center"
    )

    return fig


# ============================================================
# MISSING SKILLS CHART
# ============================================================

def create_missing_skills_chart(skills_df: pd.DataFrame, color: str, title_text: str) -> go.Figure:
    if skills_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No missing skills detected! 🎉", x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=SUCCESS))
        fig.update_layout(height=400, margin=dict(t=80, b=80, l=100, r=30), paper_bgcolor='white')
        return fig
    
    skills_df = skills_df.sort_values("importance_percent", ascending=True)
    max_val = skills_df["importance_percent"].max()
    
    if title_text == "Top 5 Missing Technical Skills":
        base_color = "#EF4444"
        colors = [f'rgba(239, 68, 68, {0.35 + (val / max_val) * 0.65})' for val in skills_df["importance_percent"]]
    else:
        base_color = "#F97316"
        colors = [f'rgba(249, 115, 22, {0.35 + (val / max_val) * 0.65})' for val in skills_df["importance_percent"]]
    
    fig = go.Figure(go.Bar(
        x=skills_df["importance_percent"],
        y=skills_df["skill"],
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=1.5), cornerradius=6),
        text=skills_df["importance_percent"].apply(lambda x: f"{x:.1f}%"),
        textposition='outside',
        textfont=dict(size=11, weight='bold', color='#1E293B'),
        hovertemplate='%{y}: %{x:.1f}% of job postings require this skill<extra></extra>',
        width=0.75
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(t=80, b=80, l=140, r=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            title="",
            gridcolor="#E2E8F0", 
            tickfont=dict(size=11, color="#475569"),
            range=[0, max_val * 1.15],
            showgrid=True,
            gridwidth=0.5,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            title="", 
            tickfont=dict(size=11, color="#334155", weight='bold'), 
            automargin=True,
            gridcolor='#E2E8F0'
        ),
        showlegend=False,
        bargap=0.3
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#E2E8F0')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#E2E8F0')
    
    fig.add_annotation(
        x=0.5, y=1.15, xref="paper", yref="paper",
        text=f"<b>{title_text}</b>",
        showarrow=False, font=dict(size=15, color="#0F172A"), align="center"
    )
    
    fig.add_annotation(
        x=0.5, y=-0.12, xref="paper", yref="paper",
        text=f"<span style='color:{base_color};font-size:14px;font-weight:bold'>●</span> <span style='font-size:13px;color:#334155;font-weight:bold'>darker: Higher Market Demand Importance (%)</span>",
        showarrow=False, font=dict(size=13, weight="bold"), align="center"
    )

    return fig


# ============================================================
# KPI CARDS
# ============================================================

def render_kpi_cards(row: pd.Series) -> None:
    overall_score = float(row.get('Final Match Score', 0) or 0)
    technical_score = float(row.get('Technical Match', 0) or 0)
    soft_score = float(row.get('Soft Skill Match', 0) or 0)
    missing_count = len(row.get("Missing Technical", [])) + len(row.get("Missing Soft", []))

    col1, col2, col3, col4 = st.columns(4, gap="large")

    cards = [
        (col1, "ATS Visibility Score", f"{overall_score:.0f}%", PRIMARY, "Strong hiring competitiveness"),
        (col2, "Technical Market Fit", f"{technical_score:.0f}%", SUCCESS, "Highest ROI improvement category"),
        (col3, "Critical Skill Gaps", f"{missing_count}", "#F97316", "Immediate attention required"),
        (col4, "Interview Readiness", f"{soft_score:.0f}%", "#A855F7", "Communication & confidence growth")
    ]

    for col, title, value, color, subtitle in cards:
        with col:
            st.markdown(f"""
            <div style="background:white; border-radius:16px; padding:20px; min-height:160px; border-left:5px solid {color}; box-shadow:0 4px 14px rgba(15,23,42,0.06);">
                <div style="font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase;">{title}</div>
                <div style="font-size:38px; font-weight:800; color:{color}; margin-top:12px;">{value}</div>
                <div style="font-size:12px; color:{color}; font-weight:700; margin-top:14px;">↗ {subtitle}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# EXECUTIVE INSIGHT BOX
# ============================================================

def render_insight_box(weakest_category: str, weakest_score: float, row: pd.Series) -> None:
    
    if weakest_category == "Technical":
        insight_text = f"Your Technical score is only {weakest_score:.0f}%. This is likely reducing ATS visibility for roles requiring programming, data analysis, or cloud skills. Recruiters often filter candidates based on technical keywords."
        recommendation = "Start with one high-demand skill from the 'Top Missing Technical Skills' section. Build a small portfolio project and add it to your resume."
    elif weakest_category == "Soft Skills":
        insight_text = f"Your Soft Skills score is only {weakest_score:.0f}%. Communication and collaboration are critical for team fit and interview success. Many qualified candidates fail interviews due to poor behavioral responses."
        recommendation = "Practice the STAR method (Situation, Task, Action, Result) for the top missing soft skills. Record yourself answering common behavioral questions."
    elif weakest_category == "Experience":
        insight_text = f"Your Experience score is only {weakest_score:.0f}%. Employers prefer candidates with relevant project or work experience. This gap often prevents getting past initial resume screening."
        recommendation = "Consider freelance projects, internships, or open-source contributions to build practical experience. Document your work in a portfolio."
    elif weakest_category == "Education":
        insight_text = f"Your Education score is only {weakest_score:.0f}%. Some roles have strict degree requirements, but many prioritize skills over formal education."
        recommendation = "Focus on certifications (AWS, Google, Microsoft) or bootcamps that demonstrate equivalent knowledge. Highlight relevant coursework and projects."
    else:
        insight_text = f"Your {weakest_category} score is only {weakest_score:.0f}%. This dimension is important for role alignment and recruiter confidence."
        recommendation = f"Review job descriptions in your target roles and identify what {weakest_category} requirements you can improve."
    
    st.markdown(f"""
    <div style="background:#EFF6FF; border-left:5px solid {PRIMARY}; border-radius:16px; padding:20px; margin:24px 0; box-shadow:0 4px 14px rgba(15,23,42,0.05);">
        <div style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:10px;">🚨 Executive Hiring Summary</div>
        <div style="font-size:13px; line-height:1.8; color:#334155;">
            <strong>🔍 Issue Identified:</strong> {insight_text}
        </div>
        <div style="margin-top:12px; padding:12px; background:white; border-radius:12px;">
            <strong style="color:{PRIMARY};">🎯 Actionable Recommendation:</strong> {recommendation}
        </div>
        <div style="margin-top:10px; font-size:12px; color:#64748B;">
            💡 Expected impact: Closing this gap could increase interview invites by +15-30%.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHART INSIGHT BOX - COMPACT VERSION
# ============================================================

def render_chart_insight(insight_key: str, color: str, **kwargs) -> None:
    
    insights = {
        "radar": {
            "title": "Hiring Strength Profile",
            "text": "Your profile shows {strongest} as your strongest dimension, while {weakest} needs improvement. Focus on the dimensions with the widest gap from 100% for maximum ROI."
        },
        "gauge": {
            "title": "Overall Candidate Readiness",
            "text": "Your overall score is {score:.0f}%, which is {level}. {next_step}"
        },
        "donut": {
            "title": "Skill Gap Distribution",
            "text": "You have {matched} matched skills and {missing} missing skills. {percentage:.0f}% of required skills are missing. Prioritize the missing skills with highest market demand."
        },
        "category": {
            "title": "Category Performance Analysis",
            "text": "Your strongest category is {strongest} ({strong_score:.0f}%). Your weakest is {weakest} ({weak_score:.0f}%). Technical and soft skills typically offer the highest ROI for improvement."
        },
        "tech_missing": {
            "title": "Critical Technical Gaps",
            "text": "The highest demand missing technical skill is '{top_skill}' ({top_pct:.1f}% of job postings). Learning this could significantly increase your interview chances."
        },
        "soft_missing": {
            "title": "Critical Behavioral Gaps",
            "text": "The highest demand missing soft skill is '{top_skill}' ({top_pct:.1f}% of job postings). Improving this will help you pass behavioral interviews."
        }
    }
    
    insight = insights.get(insight_key, insights["radar"])
    formatted_text = insight["text"].format(**kwargs)
    
    st.markdown(f"""
    <div style="background:{color}08; border-left:3px solid {color}; border-radius:10px; padding:8px 12px; margin-top:2px; margin-bottom:0px;">
        <div style="font-size:13px; font-weight:800; color:{color}; margin-bottom:4px;">📌 {insight['title']}</div>
        <div style="font-size:12px; font-weight:500; line-height:1.4; color:#334155;">{formatted_text}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ACTION CARD
# ============================================================

def render_action_card(skill_name: str, skill_type: str, actions: List[str]) -> None:
    icon = "💻" if skill_type == "technical" else "🧠"
    color = PRIMARY if skill_type == "technical" else "#A855F7"

    actions_html = "".join(f'<li style="margin:6px 0;font-size:13px;">✓ {action}</li>' for action in actions)

    st.markdown(f"""
    <div style="background:#F8FAFC; border-radius:12px; padding:14px; margin-top:12px;">
        <div style="background:{color}10; padding:8px 12px; border-radius:8px; display:inline-block; margin-bottom:12px;">
            <span style="font-size:14px; font-weight:700; color:{color};">{icon} Focus on {skill_name}</span>
        </div>
        <ul style="margin:0; padding-left:20px; color:#475569;">{actions_html}</ul>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN DASHBOARD
# ============================================================

def render_visualizations(row: pd.Series, candidate_data: Dict[str, Any]) -> None:

    # CSS to remove spacing between chart and insight box
    st.markdown("""
    <style>
        div[data-testid="stPlotlyChart"] {
            margin-bottom: -10px !important;
            padding-bottom: 0px !important;
        }
        .element-container {
            margin-bottom: 0px !important;
        }
        .stMarkdown {
            margin-top: 0px !important;
            margin-bottom: 0px !important;
        }
        div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
    <div style="margin-bottom:28px;">
        <div style="font-size:34px; font-weight:900; color:#0F172A; margin-bottom:10px;">🚀 Executive Career Intelligence Dashboard</div>
        <div style="font-size:14px; color:#64748B; line-height:1.8;">AI-powered hiring intelligence designed to identify career bottlenecks, hiring risks, and the highest ROI improvement opportunities.</div>
    </div>
    """, unsafe_allow_html=True)

    # KPI CARDS
    render_kpi_cards(row)

    # CATEGORY SCORES
    category_scores = {
        "Technical": float(row.get('Technical Match', 0) or 0),
        "Soft Skills": float(row.get('Soft Skill Match', 0) or 0),
        "Experience": float(row.get('Experience Match', 0) or 0),
        "Education": float(row.get('Education Match', 0) or 0),
        "Location": float(row.get('Location Match', 0) or 0),
        "Work Mode": float(row.get('Work Mode Match', 0) or 0),
        "Employment": float(row.get('Employment Match', 0) or 0),
        "English": float(row.get('English Match', 0) or 0),
        "Danish": float(row.get('Danish Match', 0) or 0)
    }

    weakest_category = min(category_scores, key=category_scores.get)
    weakest_score = category_scores[weakest_category]
    strongest_category = max(category_scores, key=category_scores.get)
    strongest_score = category_scores[strongest_category]

    # EXECUTIVE INSIGHT
    render_insight_box(weakest_category, weakest_score, row)

    # PRIORITY DATA
    tech_priority_df, soft_priority_df = get_missing_skills_priority(row, candidate_data)

    # Generate unique keys
    session_id = str(uuid.uuid4())[:8]

    # ===================== ROW 1 ===========================
    col1, col2 = st.columns(2)

    with col1:
        radar_fig = create_radar_chart(category_scores)
        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False}, key=f"radar_chart_{session_id}")
        render_chart_insight("radar", PRIMARY, strongest=strongest_category, weakest=weakest_category)

    with col2:
        final_score = float(row.get('Final Match Score', 0) or 0)
        gauge_fig = create_gauge_chart(final_score)
        st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False}, key=f"gauge_chart_{session_id}")
        
        if final_score < 40:
            level = "Critical - immediate action needed"
            next_step = "Focus on the highest ROI improvement areas identified below."
        elif final_score < 70:
            level = "Moderate - good foundation but gaps remain"
            next_step = "Closing technical and soft skill gaps will boost your competitiveness."
        else:
            level = "Strong - you're well positioned"
            next_step = "Maintain momentum by staying current with market trends."
        
        render_chart_insight("gauge", SUCCESS, score=final_score, level=level, next_step=next_step)

    # ===================== SPACING ===========================
    st.markdown("<br>", unsafe_allow_html=True)

    # ===================== ROW 2 ===========================
    col3, col4 = st.columns(2)

    with col3:
        tech_matched = len(row.get("Matched Technical", []))
        tech_missing = len(row.get("Missing Technical", []))
        soft_matched = len(row.get("Matched Soft", []))
        soft_missing = len(row.get("Missing Soft", []))
        
        donut_fig = create_donut_chart(tech_matched, tech_missing, soft_matched, soft_missing)
        st.plotly_chart(donut_fig, use_container_width=True, config={'displayModeBar': False}, key=f"donut_chart_{session_id}")
        
        total_matched = tech_matched + soft_matched
        total_missing = tech_missing + soft_missing
        total_skills = total_matched + total_missing
        missing_pct = (total_missing / total_skills * 100) if total_skills > 0 else 0
        
        render_chart_insight("donut", WARNING, matched=total_matched, missing=total_missing, percentage=missing_pct)

    with col4:
        bar_fig = create_category_bar_chart(category_scores)
        st.plotly_chart(bar_fig, use_container_width=True, config={'displayModeBar': False}, key=f"bar_chart_{session_id}")
        render_chart_insight("category", DANGER, strongest=strongest_category, strong_score=strongest_score, weakest=weakest_category, weak_score=weakest_score)

    # ===================== SPACING ===========================
    st.markdown("<br>", unsafe_allow_html=True)

    # ===================== ROW 3 ===========================
    col5, col6 = st.columns(2, gap="medium")

    with col5:
        if not tech_priority_df.empty:
            tech_fig = create_missing_skills_chart(tech_priority_df, PRIMARY, "Top 5 Missing Technical Skills")
            st.plotly_chart(tech_fig, use_container_width=True, config={'displayModeBar': False}, key=f"tech_skills_chart_{session_id}")
            
            top_skill = tech_priority_df.sort_values("importance_percent", ascending=False).iloc[0]["skill"]
            top_pct = tech_priority_df.sort_values("importance_percent", ascending=False).iloc[0]["importance_percent"]
            
            render_chart_insight("tech_missing", PRIMARY, top_skill=top_skill, top_pct=top_pct)
            render_action_card(top_skill, "technical", [
                f"Take a course or certification in {top_skill}",
                f"Build a small portfolio project using {top_skill}",
                f"Add {top_skill} to your resume and LinkedIn",
                "Practice technical interview questions on this skill"
            ])
        else:
            st.info("🎉 No missing technical skills detected!")

    with col6:
        if not soft_priority_df.empty:
            soft_fig = create_missing_skills_chart(soft_priority_df, PURPLE, "Top 5 Missing Soft Skills")
            st.plotly_chart(soft_fig, use_container_width=True, config={'displayModeBar': False}, key=f"soft_skills_chart_{session_id}")
            
            top_skill = soft_priority_df.sort_values("importance_percent", ascending=False).iloc[0]["skill"]
            top_pct = soft_priority_df.sort_values("importance_percent", ascending=False).iloc[0]["importance_percent"]
            
            render_chart_insight("soft_missing", PURPLE, top_skill=top_skill, top_pct=top_pct)
            render_action_card(top_skill, "soft", [
                f"Prepare STAR stories demonstrating {top_skill}",
                f"Join a group project or team activity to practice {top_skill}",
                f"Ask for feedback on your {top_skill} skills from peers",
                "Record yourself answering behavioral questions"
            ])
        else:
            st.info("🎉 No missing soft skills detected!")

    # FOOTER
    final_score = float(row.get('Final Match Score', 0) or 0)
    total_missing = len(row.get("Missing Technical", [])) + len(row.get("Missing Soft", []))

    recommendation_text = ""
    ats_rank = ""
    ats_description = ""
    rank_color = ""

    if final_score < 40:
        recommendation_text = "Your readiness score needs significant improvement. Start with the highest-demand missing skill. Consistent practice and building a portfolio project will make you more competitive."
        ats_rank = "Bottom 25%"
        ats_description = "Your profile ranks below most candidates. Significant improvements needed to pass ATS screening."
        rank_color = "#EF4444"
    elif final_score < 55:
        recommendation_text = "You have room for improvement. Focus on the top missing skills to move above average."
        ats_rank = "Bottom 40%"
        ats_description = "Your profile ranks below average. Focus on closing the identified skill gaps."
        rank_color = "#F59E0B"
    elif final_score < 70:
        recommendation_text = "You have a solid foundation. Prioritize the top missing skills from each category and work on practical projects."
        ats_rank = "Top 50%"
        ats_description = "Your profile is average compared to other candidates. Closing key gaps will move you to top tier."
        rank_color = "#F59E0B"
    elif final_score < 85:
        recommendation_text = "You're doing well! Focus on advanced skills and stay updated with industry trends."
        ats_rank = "Top 25%"
        ats_description = "Your profile ranks above most candidates. You're competitive with room for improvement."
        rank_color = "#10B981"
    else:
        recommendation_text = "Excellent work! Maintain your edge by staying current with market trends and advanced certifications."
        ats_rank = "Top 10%"
        ats_description = "Your profile ranks among the best candidates. Excellent market positioning!"
        rank_color = "#10B981"

    st.markdown(f"""
    <div style="background:white; border-radius:16px; padding:20px 24px; text-align:center; border:1px solid #E2E8F0; margin-top:8px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="font-size:16px; font-weight:800; color:#0F172A; margin-bottom:8px;">🔍 Executive Recommendation</div>
        <div style="font-size:15px; font-weight:500; color:#334155; line-height:1.5; margin-bottom:16px;">{recommendation_text}</div>
        <div style="display:inline-block; background:{rank_color}10; border-left:3px solid {rank_color}; padding:10px 20px; border-radius:10px; text-align:left;">
            <div style="font-size:14px; font-weight:700; color:{rank_color};">ATS Ranking: {ats_rank}</div>
            <div style="font-size:12px; font-weight:500; color:#475569; margin-top:4px;">{ats_description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)