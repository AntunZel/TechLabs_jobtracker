import streamlit as st


# ==========================================================
#  ROADMAP RECOMMENDATION HELPERS
# ==========================================================

def location_recommendations(score):

    if score >= 95:

        return [
            "Your preferred location already aligns very well with this role"
        ]

    elif score >= 70:

        return [
            "Stay flexible with nearby opportunities",
            "Consider hybrid work arrangements"
        ]

    else:

        return [
            "Expand your job search flexibility",
            "Consider relocation or remote opportunities",
            "Explore additional nearby job markets"
        ]


def employment_recommendations(score):

    if score >= 95:

        return [
            "Your employment preference aligns strongly with this opportunity"
        ]

    elif score >= 70:

        return [
            "Stay open to flexible work arrangements",
            "Explore similar employment models"
        ]

    else:

        return [
            "Consider broader employment opportunities",
            "Explore internship or flexible work options",
            "Stay open to alternative work arrangements"
        ]


def education_recommendations(score):

    if score >= 95:

        return [
            "Your educational background already matches this role very well"
        ]

    elif score >= 70:

        return [
            "Continue strengthening practical industry experience",
            "Consider additional certifications"
        ]

    else:

        return [
            "Explore certifications and advanced learning paths",
            "Strengthen practical project experience",
            "Continue improving technical specialization"
        ]


def experience_recommendations(score):

    if score >= 95:

        return [
            "Your experience level strongly aligns with this opportunity"
        ]

    elif score >= 70:

        return [
            "Continue building practical project experience",
            "Strengthen real-world business exposure"
        ]

    else:

        return [
            "Build more hands-on projects",
            "Gain additional real-world experience",
            "Contribute to practical business case studies"
        ]


def english_recommendations(score):

    if score >= 95:

        return [
            "Your English communication already aligns very well with this role"
        ]

    elif score >= 70:

        return [
            "Continue improving professional English communication",
            "Practice technical interview conversations"
        ]

    else:

        return [
            "Improve business English communication",
            "Practice technical interview conversations",
            "Strengthen workplace English fluency"
        ]


def danish_recommendations(score):

    if score >= 95:

        return [
            "Your Danish communication already aligns well with this role"
        ]

    elif score >= 70:

        return [
            "Continue improving workplace Danish communication",
            "Practice professional Danish conversations"
        ]

    else:

        return [
            "Strengthen professional Danish vocabulary",
            "Practice workplace Danish conversations",
            "Improve daily Danish communication skills"
        ]

# ============================================================
# SUCCESS ROADMAP
# ============================================================

def render_success_roadmap(row):

    # SECTION DIVIDER
    st.markdown("""
    <hr style="
    margin-top:50px;
    margin-bottom:45px;
    border:none;
    border-top:2px solid rgba(0,0,0,0.12);
    ">
    """, unsafe_allow_html=True)

    # SECTION TITLE
    st.markdown(
        '<div class="section-title">🚀 Personalized Success Roadmap</div>',
        unsafe_allow_html=True
    )

    # INTRO TEXT
    st.markdown("""
    <div style="
    font-size:18px;
    line-height:2;
    color:#475569;
    margin-bottom:35px;
    ">

    Based on your current profile and skill gaps, here are some personalized recommendations
    that can help you become a stronger match for this opportunity.

    </div>
    """, unsafe_allow_html=True)


    # TECHNICAL SKILL RECOMMENDATIONS
    technical_skill_recommendations = {

        "sql":
            "Practice advanced SQL queries and real-world analytics",

        "sql basics":
            "Strengthen SQL fundamentals with hands-on exercises",

        "excel":
            "Improve Excel reporting and analytical workflows",

        "advanced excel":
            "Improve advanced Excel analytics and automation skills",

        "power bi":
            "Build interactive Power BI dashboards and KPIs",

        "power query":
            "Practice data transformation with Power Query",

        "tableau":
            "Improve storytelling and dashboard visualization skills",

        "reporting":
            "Practice business reporting and insight generation",

        "dashboard optimization":
            "Improve dashboard performance and UX design",

        "visualization":
            "Improve data visualization and storytelling techniques",

        "data storytelling":
            "Improve storytelling with data and visual insights",

        "dax":
            "Practice advanced DAX measures and calculations",

        "google analytics":
            "Practice web and customer analytics with Google Analytics",

        "python":
            "Build real-world Python data projects",

        "python basics":
            "Strengthen Python fundamentals with practical exercises",

        "pandas":
            "Practice data cleaning and transformation with Pandas",

        "numpy":
            "Improve analytical programming with NumPy",

        "matplotlib":
            "Improve data visualization with Matplotlib",

        "seaborn":
            "Practice advanced data storytelling with Seaborn",

        "etl pipeline design":
            "Build scalable ETL pipeline projects",

        "data pipelines":
            "Build scalable production-style data pipelines",

        "airflow":
            "Learn workflow orchestration with Apache Airflow",

        "spark":
            "Practice big data processing with PySpark",

        "kafka":
            "Practice event streaming and real-time data pipelines",

        "apache kafka":
            "Learn real-time data streaming with Apache Kafka",

        "data warehousing":
            "Improve dimensional modeling and warehousing concepts",

        "data modeling":
            "Practice database and analytical data modeling",

        "machine learning":
            "Build practical machine learning projects",

        "tensorflow":
            "Build deep learning projects using TensorFlow",

        "pytorch":
            "Practice neural network development with PyTorch",

        "scikit-learn":
            "Improve classical machine learning workflows",

        "deep learning":
            "Build deep learning and neural network projects",

        "computer vision":
            "Build computer vision and image-processing projects",

        "nlp":
            "Build natural language processing applications",

        "mlops":
            "Practice MLOps workflows and ML deployment pipelines",

        "docker":
            "Build containerized applications with Docker",

        "docker basics":
            "Move beyond Docker basics with hands-on container projects",

        "kubernetes":
            "Practice container orchestration with Kubernetes",

        "terraform":
            "Build Infrastructure as Code projects using Terraform",

        "aws":
            "Improve AWS cloud and data engineering skills",

        "azure":
            "Practice cloud architecture and deployment on Azure",

        "cloud security":
            "Improve cloud security and infrastructure protection skills",

        "linux":
            "Practice Linux command-line and server management skills",

        "git":
            "Improve Git version control and collaboration workflows",

        "jenkins":
            "Practice CI/CD automation with Jenkins",

        "ci/cd":
            "Build CI/CD workflows and deployment automation",

        "streamlit":
            "Create interactive data applications with Streamlit",

        "figma":
            "Practice UI/UX design and prototyping with Figma",

        "wireframing":
            "Improve low-fidelity and high-fidelity wireframing skills"
    }


    # SOFT SKILL RECOMMENDATIONS
    soft_skill_recommendations = {

        "problem solving":
            "Practice analytical and problem-solving scenarios",

        "stakeholder communication":
            "Improve stakeholder communication and business alignment",

        "adaptability":
            "Practice working effectively in fast-changing environments",

        "critical thinking":
            "Strengthen critical thinking and decision-making skills",

        "analytical thinking":
            "Improve analytical reasoning and business analysis skills",

        "attention to detail":
            "Practice delivering accurate and detail-oriented work",

        "teamwork":
            "Improve collaboration and teamwork experience",

        "leadership":
            "Develop leadership and project ownership skills",

        "presentation skills":
            "Practice public speaking and presentation delivery",

        "time management":
            "Practice prioritization and time management skills",

        "creativity":
            "Practice creative problem solving and ideation",

        "project management":
            "Improve planning and project execution skills",

        "communication":
            "Improve professional communication and collaboration skills"
    }


    # DYNAMIC ROADMAP GENERATION
    technical_roadmap = []

    soft_roadmap = []

    # TECHNICAL ROADMAP
    for skill in row["Missing Technical"]:

        skill_lower = skill.lower()

        recommendation = technical_skill_recommendations.get(

            skill_lower,

            f"Strengthen your {skill} skills with practical real-world projects and hands-on experience"
        )

        technical_roadmap.append(recommendation)


    # SOFT ROADMAP
    for skill in row["Missing Soft"]:

        skill_lower = skill.lower()

        recommendation = soft_skill_recommendations.get(

            skill_lower,

            f"Continue improving your {skill} skills through teamwork, collaboration, and practical experience"
        )

        soft_roadmap.append(recommendation)


    # FALLBACKS
    if len(technical_roadmap) == 0:

        technical_roadmap = [

            "Your technical skills already match this opportunity very well"
        ]


    if len(soft_roadmap) == 0:

        soft_roadmap = [

            "Your soft skills already align strongly with this role"
        ]


    # ROADMAP SECTIONS
    roadmap_sections = [

        (
            "💻 Technical Skills Improvements",

            row['Technical Match'],

            technical_roadmap
        ),

        (
            "👥 Soft Skills Improvements",

            row['Soft Skill Match'],

            soft_roadmap
        ),

        (
            "📍 Location Improvements",

            row['Location Match'],

            location_recommendations(
                row['Location Match']
            )
        ),

        (
            "💼 Employment Recommendations",

            row['Employment Match'],

            employment_recommendations(
                row['Employment Match']
            )
        ),

        (
            "🎓 Education Recommendations",

            row['Education Match'],

            education_recommendations(
                row['Education Match']
            )
        ),

        (
            "🧠 Experience Recommendations",

            row['Experience Match'],

            experience_recommendations(
                row['Experience Match']
            )
        ),

        (
            "🗣️ English Recommendations",

            row['English Match'],

            english_recommendations(
                row['English Match']
            )
        ),

        (
            "🌍 Danish Recommendations",

            row['Danish Match'],

            danish_recommendations(
                row['Danish Match']
            )
        )
    ]

    # SHOW ONLY IMPROVEMENT AREAS
    roadmap_sections = [

        section

        for section in roadmap_sections

        if section[1] < 95
    ]


    # RENDER ROADMAP
    for title, score, recommendations in roadmap_sections:

        section_title_html = f"""
        <div style="
        margin-top:30px;
        margin-bottom:14px;
        font-size:28px;
        font-weight:900;
        color:#111827;
        ">

        {title} — {score}%

        </div>
        """

        st.markdown(
            section_title_html,
            unsafe_allow_html=True
        )


        for item in recommendations:

            recommendation_html = f"""
            <div style="
            margin-left:18px;
            margin-bottom:10px;
            font-size:18px;
            line-height:1.9;
            color:#374151;
            ">

            • {item}

            </div>
            """

            st.markdown(
                recommendation_html,
                unsafe_allow_html=True
            )


        st.markdown("""
        <hr style="
        margin-top:25px;
        margin-bottom:25px;
        border:none;
        border-top:1px solid rgba(0,0,0,0.08);
        ">
        """, unsafe_allow_html=True)



