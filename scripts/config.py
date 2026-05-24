# MATCHING WEIGHTS

SIMILARITY_WEIGHT = 0.35

TECHNICAL_SKILL_WEIGHT = 0.20

SOFT_SKILL_WEIGHT = 0.10

EXPERIENCE_WEIGHT = 0.10

EDUCATION_WEIGHT = 0.08

ENGLISH_WEIGHT = 0.05

DANISH_WEIGHT = 0.05

LOCATION_WEIGHT = 0.03

WORK_MODE_WEIGHT = 0.02

EMPLOYMENT_WEIGHT = 0.02


# THRESHOLDS

EXCELLENT_MATCH_THRESHOLD = 95

GOOD_MATCH_THRESHOLD = 70


# CHART SETTINGS

# DEFAULT_CHART_HEIGHT = 450

# LARGE_CHART_HEIGHT = 500


# SYSTEM

TOP_RECOMMENDATIONS_COUNT = 5


# ============================================================
# ROLE SKILL WEIGHTS
# ============================================================

ROLE_SKILL_WEIGHTS = {

    # ========================================================
    # DATA ANALYST
    # ========================================================

    "Data Analyst": {

        # Technical Skills
        "sql": 10,
        "power bi": 10,
        "excel": 9,
        "python": 8,
        "statistics": 9,
        "tableau": 7,
        "data visualization": 9,
        "data cleaning": 8,
        "a/b testing": 7,
        "forecasting": 7,
        "kpi analysis": 8,
        "dax": 8,

        # Soft Skills
        "analytical thinking": 10,
        "business understanding": 9,
        "communication": 8,
        "storytelling": 8,
        "presentation skills": 7,
        "collaboration": 7,
        "attention to detail": 8
    },


    # ========================================================
    # DATA ENGINEER
    # ========================================================

    "Data Engineer": {

        # Technical Skills
        "python": 10,
        "sql": 10,
        "spark": 10,
        "kafka": 10,
        "airflow": 9,
        "docker": 9,
        "kubernetes": 8,
        "linux": 9,
        "aws": 8,
        "terraform": 7,
        "hadoop": 7,
        "nosql": 7,
        "etl": 9,
        "snowflake": 7,

        # Soft Skills
        "problem solving": 9,
        "adaptability": 7,
        "teamwork": 7,
        "communication": 6,
        "attention to detail": 8
    },


    # ========================================================
    # BI
    # ========================================================

    "BI": {

        # Technical Skills
        "power bi": 10,
        "tableau": 9,
        "sql": 9,
        "excel": 9,
        "dax": 10,
        "kpi analysis": 9,
        "data visualization": 10,
        "reporting tools": 8,
        "forecasting": 7,

        # Soft Skills
        "business understanding": 10,
        "communication": 8,
        "storytelling": 9,
        "presentation skills": 8,
        "decision making": 8,
        "collaboration": 7
    },


    # ========================================================
    # DEVOPS
    # ========================================================

    "DevOps": {

        # Technical Skills
        "docker": 10,
        "kubernetes": 10,
        "linux": 10,
        "terraform": 9,
        "jenkins": 9,
        "aws": 9,
        "ansible": 8,
        "bash": 8,
        "python": 7,
        "networking": 7,
        "git": 7,
        "prometheus": 8,
        "grafana": 8,

        # Soft Skills
        "problem solving": 9,
        "adaptability": 8,
        "teamwork": 7,
        "communication": 7
    },


    # ========================================================
    # ML / AI
    # ========================================================

    "ML/AI": {

        # Technical Skills
        "python": 10,
        "tensorflow": 9,
        "pytorch": 9,
        "scikit-learn": 10,
        "statistics": 9,
        "feature engineering": 8,
        "data preprocessing": 8,
        "sql": 7,
        "nlp": 7,
        "computer vision": 7,
        "xgboost": 8,
        "pandas": 8,
        "numpy": 8,

        # Soft Skills
        "analytical thinking": 10,
        "problem solving": 9,
        "research mindset": 8,
        "creativity": 7,
        "communication": 6
    },


    # ========================================================
    # UX
    # ========================================================

    "UX": {

        # Technical Skills
        "figma": 10,
        "wireframing": 9,
        "prototyping": 9,
        "user research": 10,
        "ui design": 9,
        "interaction design": 8,
        "usability testing": 8,
        "design systems": 7,

        # Soft Skills
        "communication": 9,
        "creativity": 10,
        "empathy": 10,
        "collaboration": 8,
        "presentation skills": 7,
        "problem solving": 7
    }
}
