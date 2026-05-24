import streamlit as st


def render_match_analysis(row):

    # --------------------------------------------------------
    # SECTION TITLE
    # --------------------------------------------------------

    st.markdown("""
    <div class="section-title">

    📊 Match Analysis

    </div>
    """, unsafe_allow_html=True)

    # MAIN MATCH SCORES
    scores = [

        (
            "🟢 Final Match",
            row['Final Match Score'],
            "#22c55e"
        ),

        (
            "🔵 Technical Match",
            row['Technical Match'],
            "#3b82f6"
        ),

        (
            "🟣 Soft Skill Match",
            row['Soft Skill Match'],
            "#8b5cf6"
        ),
    ]


    for label, value, color in scores:

        font_size = (
            "38px"
            if "Final" in label
            else "18px"
        )

        bar_height = (
            "22px"
            if "Final" in label
            else "16px"
        )

        st.markdown(f"""
        <div style="
        margin-bottom:28px;
        ">

        <div style="
        font-size:{font_size};
        font-weight:900;
        color:{color};
        margin-bottom:10px;
        ">

        {label}: {value}%

        </div>

        <div style="
        width:100%;
        height:{bar_height};
        background:#e5e7eb;
        border-radius:12px;
        overflow:hidden;
        ">

        <div style="
        width:{value}%;
        height:{bar_height};
        background:{color};
        border-radius:12px;
        ">
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)


    # SMALL METRICS
    metric_col1, metric_col2 = st.columns(2)


    # EXPERIENCE MATCH
    with metric_col1:

        st.markdown(f"""
        <div style="
        background:white;
        padding:10px 22px;
        border-radius:16px;
        margin-top:10px;
        margin-bottom:18px;
        border-left:5px solid #f97316;
        box-shadow:0 2px 10px rgba(0,0,0,0.05);
        ">

        <div style="
        font-size:14px;
        font-weight:700;
        color:#111827;
        margin-bottom:8px;
        ">

        🟠 Experience Match

        </div>

        <div style="
        font-size:28px;
        font-weight:900;
        color:#0f172a;
        ">

        {row['Experience Match']}%

        </div>

        </div>
        """, unsafe_allow_html=True)


    # EDUCATION MATCH
    with metric_col2:

        st.markdown(f"""
        <div style="
        background:white;
        padding:10px 22px;
        border-radius:16px;
        margin-top:10px;
        margin-bottom:18px;
        border-left:5px solid #14b8a6;
        box-shadow:0 2px 10px rgba(0,0,0,0.05);
        ">

        <div style="
        font-size:14px;
        font-weight:800;
        color:#111827;
        margin-bottom:8px;
        ">

        🎓 Education Match

        </div>

        <div style="
        font-size:28px;
        font-weight:900;
        color:#0f172a;
        ">

        {row['Education Match']}%

        </div>

        </div>
        """, unsafe_allow_html=True)

    # MATCH BADGES
    badge_html = ""

    if row['Location Match'] >= 100:

        badge_html += (
            '<span class="skill-pill-green">'
            '📍 Location Match'
            '</span>'
        )

    if row['Work Mode Match'] >= 100:

        badge_html += (
            '<span class="skill-pill-green">'
            '🏠 Work Mode Match'
            '</span>'
        )

    if row['English Match'] >= 100:

        badge_html += (
            '<span class="skill-pill-green">'
            '🗣️ English Match'
            '</span>'
        )

    if row['Danish Match'] >= 100:

        badge_html += (
            '<span class="skill-pill-green">'
            '🗣️ Danish Match'
            '</span>'
        )

    if row['Employment Match'] >= 100:

        badge_html += (
            '<span class="skill-pill-green">'
            '💼 Employment Match'
            '</span>'
        )

    # RENDER BADGES
    st.markdown(
        f"""
    <div style="
    margin-top:18px;
    margin-bottom:28px;
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    align-items:center;
    justify-content:flex-start;
    align-content:flex-start;
    width:100%;
    ">

    {badge_html}

    </div>
    """,
        unsafe_allow_html=True
    )

