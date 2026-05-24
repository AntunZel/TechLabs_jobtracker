# ============================================================
# skill_gap_analysis.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import uuid


def render_skill_gap_analysis(row, candidate_data=None):
    """
    Render skill gap analysis with separate heatmaps for technical and soft skills
    Args:
        row: DataFrame row containing skill data
        candidate_data: Dictionary containing candidate info (optional)
    """
    
    # Create unique keys for each run
    unique_id = str(uuid.uuid4())[:8]
    
    # Default value if candidate_data not provided
    if candidate_data is None:
        candidate_data = {"preferred_roles": []}
    
    # --------------------------------------------------------
    # SECTION DIVIDER
    # --------------------------------------------------------

    st.markdown("""
    <hr style="margin-top:40px; margin-bottom:40px; border:none; border-top:2px solid rgba(0,0,0,0.08);">
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # SECTION TITLE WITH COUNTER
    # --------------------------------------------------------
    
    total_matched = len(row.get("Matched Technical", [])) + len(row.get("Matched Soft", []))
    total_missing = len(row.get("Missing Technical", [])) + len(row.get("Missing Soft", []))
    total_skills = total_matched + total_missing
    match_rate = (total_matched / total_skills * 100) if total_skills > 0 else 0
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:24px;">
        <div>
            <div style="font-size:28px; font-weight:800; color:#0F172A;">🧠 Skill Gap Analysis</div>
            <div style="font-size:14px; color:#64748B; margin-top:4px;">Comprehensive breakdown of your technical and behavioral skills</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:32px; font-weight:800; color:#0F172A;">{match_rate:.0f}%</div>
            <div style="font-size:12px; color:#64748B;">Overall Match Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall progress bar
    st.markdown(f"""
    <div style="background:#E2E8F0; border-radius:10px; height:8px; margin-bottom:32px; overflow:hidden;">
        <div style="background:linear-gradient(90deg, #10B981, #34D399); width:{match_rate}%; height:100%; border-radius:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # TWO COLUMN LAYOUT FOR TECHNICAL AND SOFT SKILLS
    # ========================================================
    
    col1, col2 = st.columns(2, gap="large")
    
    # ========================================================
    # TECHNICAL SKILLS COLUMN
    # ========================================================
    
    with col1:
        tech_matched = len(row.get("Matched Technical", []))
        tech_missing = len(row.get("Missing Technical", []))
        tech_total = tech_matched + tech_missing
        tech_match_rate = (tech_matched / tech_total * 100) if tech_total > 0 else 0
        
        st.markdown(f"""
        <div style="background:white; border-radius:20px; padding:20px; border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(0,0,0,0.04); height:100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <div>
                    <div style="font-size:18px; font-weight:800; color:#2563EB;">💻 Technical Skills</div>
                    <div style="font-size:13px; color:#64748B; margin-top:2px;">{tech_matched} matched · {tech_missing} missing</div>
                </div>
                <div style="background:#2563EB10; padding:8px 16px; border-radius:30px;">
                    <span style="font-size:20px; font-weight:800; color:#2563EB;">{tech_match_rate:.0f}%</span>
                </div>
            </div>
            <div style="background:#E2E8F0; border-radius:8px; height:6px; margin-bottom:20px; overflow:hidden;">
                <div style="background:#2563EB; width:{tech_match_rate}%; height:100%; border-radius:8px;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Matched Technical Skills
        st.markdown('<div style="font-size:14px; font-weight:700; color:#10B981; margin-bottom:10px;">✓ Matched Skills</div>', unsafe_allow_html=True)
        
        if row.get("Matched Technical", []):
            matched_html = "".join(f'<span style="display:inline-block; background:#DCFCE7; color:#166534; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; margin:4px;">{skill}</span>' for skill in row["Matched Technical"])
            st.markdown(f'<div style="margin-bottom:20px;">{matched_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:13px; margin-bottom:20px;">No matched technical skills</div>', unsafe_allow_html=True)
        
        # Missing Technical Skills
        st.markdown('<div style="font-size:14px; font-weight:700; color:#EF4444; margin-bottom:10px;">✗ Missing Skills</div>', unsafe_allow_html=True)
        
        if row.get("Missing Technical", []):
            missing_html = "".join(f'<span style="display:inline-block; background:#FEE2E2; color:#991B1B; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; margin:4px;">{skill}</span>' for skill in row["Missing Technical"])
            st.markdown(f'<div>{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:13px;">No missing technical skills! 🎉</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================
    # SOFT SKILLS COLUMN
    # ========================================================
    
    with col2:
        soft_matched = len(row.get("Matched Soft", []))
        soft_missing = len(row.get("Missing Soft", []))
        soft_total = soft_matched + soft_missing
        soft_match_rate = (soft_matched / soft_total * 100) if soft_total > 0 else 0
        
        st.markdown(f"""
        <div style="background:white; border-radius:20px; padding:20px; border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(0,0,0,0.04); height:100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <div>
                    <div style="font-size:18px; font-weight:800; color:#8B5CF6;">🧠 Soft Skills</div>
                    <div style="font-size:13px; color:#64748B; margin-top:2px;">{soft_matched} matched · {soft_missing} missing</div>
                </div>
                <div style="background:#8B5CF610; padding:8px 16px; border-radius:30px;">
                    <span style="font-size:20px; font-weight:800; color:#8B5CF6;">{soft_match_rate:.0f}%</span>
                </div>
            </div>
            <div style="background:#E2E8F0; border-radius:8px; height:6px; margin-bottom:20px; overflow:hidden;">
                <div style="background:#8B5CF6; width:{soft_match_rate}%; height:100%; border-radius:8px;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Matched Soft Skills
        st.markdown('<div style="font-size:14px; font-weight:700; color:#10B981; margin-bottom:10px;">✓ Matched Skills</div>', unsafe_allow_html=True)
        
        if row.get("Matched Soft", []):
            matched_html = "".join(f'<span style="display:inline-block; background:#DCFCE7; color:#166534; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; margin:4px;">{skill}</span>' for skill in row["Matched Soft"])
            st.markdown(f'<div style="margin-bottom:20px;">{matched_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:13px; margin-bottom:20px;">No matched soft skills</div>', unsafe_allow_html=True)
        
        # Missing Soft Skills
        st.markdown('<div style="font-size:14px; font-weight:700; color:#EF4444; margin-bottom:10px;">✗ Missing Skills</div>', unsafe_allow_html=True)
        
        if row.get("Missing Soft", []):
            missing_html = "".join(f'<span style="display:inline-block; background:#FEE2E2; color:#991B1B; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; margin:4px;">{skill}</span>' for skill in row["Missing Soft"])
            st.markdown(f'<div>{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:13px;">No missing soft skills! 🎉</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================
    # HEATMAP - SEPARATE FOR TECHNICAL AND SOFT SKILLS
    # ========================================================
    
    selected_roles = candidate_data.get("preferred_roles", [])
    
    if selected_roles:
        st.markdown("""
        <div style="margin-top:32px; margin-bottom:16px;">
            <div style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:4px;">🔥 Skill Priority Heatmap</div>
            <div style="font-size:13px; color:#64748B;">Darker color = higher market demand for your target roles</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Load importance data from CSV files
        try:
            from .visualizations import load_technical_skills, load_soft_skills
        except ImportError:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from ui.visualizations import load_technical_skills, load_soft_skills
        
        tech_df = load_technical_skills()
        soft_df = load_soft_skills()
        
        # Filter by selected roles
        tech_role_df = tech_df[tech_df["role_category"].isin(selected_roles)]
        soft_role_df = soft_df[soft_df["role_category"].isin(selected_roles)]
        
        # Aggregate importance for technical skills
        tech_importance = tech_role_df.groupby("skill")["technical_skills_required"].sum().reset_index()
        tech_importance.columns = ["skill", "importance"]
        total_tech = tech_importance["importance"].sum()
        if total_tech > 0:
            tech_importance["importance_pct"] = tech_importance["importance"] / total_tech * 100
        else:
            tech_importance["importance_pct"] = 0
        
        # Aggregate importance for soft skills
        soft_importance = soft_role_df.groupby("skill")["soft_skills_required"].sum().reset_index()
        soft_importance.columns = ["skill", "importance"]
        total_soft = soft_importance["importance"].sum()
        if total_soft > 0:
            soft_importance["importance_pct"] = soft_importance["importance"] / total_soft * 100
        else:
            soft_importance["importance_pct"] = 0
        
        # Get missing skills with their importance
        missing_tech_importance = tech_importance[tech_importance["skill"].str.lower().isin([s.lower() for s in row.get("Missing Technical", [])])].sort_values("importance_pct", ascending=False)
        missing_soft_importance = soft_importance[soft_importance["skill"].str.lower().isin([s.lower() for s in row.get("Missing Soft", [])])].sort_values("importance_pct", ascending=False)
        
        # ==================== TECHNICAL SKILLS HEATMAP (RED) ====================
        if not missing_tech_importance.empty:
            st.markdown(f"""
            <div style="margin-top:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">💻</span>
                    <span style="font-size:16px; font-weight:700; color:#EF4444;">Missing Technical Skills Priority</span>
                    <span style="font-size:12px; color:#64748B; margin-left:8px;">({len(missing_tech_importance)} missing skills)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_tech = px.bar(
                missing_tech_importance,
                x="importance_pct",
                y="skill",
                orientation='h',
                color="importance_pct",
                color_continuous_scale=['#FEE2E2', '#EF4444', '#DC2626', '#991B1B'],
                labels={"importance_pct": "Market Demand Importance (%)", "skill": ""},
                text="importance_pct"
            )
            
            fig_tech.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker=dict(line=dict(color='white', width=1.5), cornerradius=6),
                hovertemplate='%{y}: %{x:.1f}% demand<extra></extra>'
            )
            
            fig_tech.update_layout(
                height=300,
                margin=dict(t=30, b=20, l=120, r=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Market Demand Importance (%)",
                xaxis=dict(gridcolor="#E2E8F0", range=[0, max(missing_tech_importance["importance_pct"]) * 1.15]),
                coloraxis_colorbar=dict(title="Priority", tickfont=dict(size=10)),
                showlegend=False
            )
            
            st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False}, key=f"tech_priority_heatmap_{unique_id}")
            
            # Top skill insight for technical
            top_tech = missing_tech_importance.iloc[0]["skill"] if not missing_tech_importance.empty else None
            top_tech_pct = missing_tech_importance.iloc[0]["importance_pct"] if not missing_tech_importance.empty else 0
            
            if top_tech:
                st.markdown(f"""
                <div style="background:#FEF2F2; border-left:4px solid #EF4444; border-radius:8px; padding:8px 12px; margin-top:8px;">
                    <span style="font-size:12px; color:#EF4444;">🎯 <strong>Priority:</strong> {top_tech} ({top_tech_pct:.1f}% demand)</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin-top:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">💻</span>
                    <span style="font-size:16px; font-weight:700; color:#2563EB;">Technical Skills</span>
                    <span style="font-size:12px; color:#10B981; margin-left:8px;">✅ No missing technical skills!</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ==================== SOFT SKILLS HEATMAP (ORANGE) ====================
        if not missing_soft_importance.empty:
            st.markdown(f"""
            <div style="margin-top:32px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">🧠</span>
                    <span style="font-size:16px; font-weight:700; color:#F97316;">Missing Soft Skills Priority</span>
                    <span style="font-size:12px; color:#64748B; margin-left:8px;">({len(missing_soft_importance)} missing skills)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_soft = px.bar(
                missing_soft_importance,
                x="importance_pct",
                y="skill",
                orientation='h',
                color="importance_pct",
                color_continuous_scale=['#FEF3C7', '#F97316', '#EA580C', '#9A3412'],
                labels={"importance_pct": "Market Demand Importance (%)", "skill": ""},
                text="importance_pct"
            )
            
            fig_soft.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker=dict(line=dict(color='white', width=1.5), cornerradius=6),
                hovertemplate='%{y}: %{x:.1f}% demand<extra></extra>'
            )
            
            fig_soft.update_layout(
                height=300,
                margin=dict(t=30, b=20, l=120, r=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Market Demand Importance (%)",
                xaxis=dict(gridcolor="#E2E8F0", range=[0, max(missing_soft_importance["importance_pct"]) * 1.15]),
                coloraxis_colorbar=dict(title="Priority", tickfont=dict(size=10)),
                showlegend=False
            )
            
            st.plotly_chart(fig_soft, use_container_width=True, config={'displayModeBar': False}, key=f"soft_priority_heatmap_{unique_id}")
            
            # Top skill insight for soft
            top_soft = missing_soft_importance.iloc[0]["skill"] if not missing_soft_importance.empty else None
            top_soft_pct = missing_soft_importance.iloc[0]["importance_pct"] if not missing_soft_importance.empty else 0
            
            if top_soft:
                st.markdown(f"""
                <div style="background:#FFF7ED; border-left:4px solid #F97316; border-radius:8px; padding:8px 12px; margin-top:8px;">
                    <span style="font-size:12px; color:#F97316;">🎯 <strong>Priority:</strong> {top_soft} ({top_soft_pct:.1f}% demand)</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin-top:32px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">🧠</span>
                    <span style="font-size:16px; font-weight:700; color:#8B5CF6;">Soft Skills</span>
                    <span style="font-size:12px; color:#10B981; margin-left:8px;">✅ No missing soft skills!</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================
    # GAP SUMMARY CARD
    # ========================================================
    
    if total_missing > 0:
        tech_total_skills = len(row.get("Matched Technical", [])) + len(row.get("Missing Technical", []))
        soft_total_skills = len(row.get("Matched Soft", [])) + len(row.get("Missing Soft", []))
        
        tech_gap_pct = (len(row.get("Missing Technical", [])) / tech_total_skills * 100) if tech_total_skills > 0 else 0
        soft_gap_pct = (len(row.get("Missing Soft", [])) / soft_total_skills * 100) if soft_total_skills > 0 else 0
        
        st.markdown(f"""
        <div style="background:#F8FAFC; border-radius:16px; padding:20px; border:1px solid #E2E8F0; margin-top:24px;">
            <div style="display:flex; gap:20px; justify-content:space-around;">
                <div style="text-align:center;">
                    <div style="font-size:28px; font-weight:800; color:#EF4444;">{tech_gap_pct:.0f}%</div>
                    <div style="font-size:12px; color:#64748B;">Technical Gap</div>
                </div>
                <div style="width:1px; background:#E2E8F0;"></div>
                <div style="text-align:center;">
                    <div style="font-size:28px; font-weight:800; color:#EF4444;">{soft_gap_pct:.0f}%</div>
                    <div style="font-size:12px; color:#64748B;">Soft Skills Gap</div>
                </div>
                <div style="width:1px; background:#E2E8F0;"></div>
                <div style="text-align:center;">
                    <div style="font-size:28px; font-weight:800; color:#F59E0B;">{total_missing}</div>
                    <div style="font-size:12px; color:#64748B;">Total Gaps</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)