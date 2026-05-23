import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
import json

EDUCATION_LEVELS = ["high_school", "associate", "bachelor", "master", "phd", "bootcamp"]
FIELDS_OF_STUDY  = ["cs", "data_science", "engineering", "business", "design",
                     "natural_sci", "social_sci", "humanities", "medicine", "law", "other"]
TECH_SKILLS      = ["python", "sql", "ml", "js", "cloud", "excel", "bi", "java",
                     "design_tools", "devops", "stats"]
SOFT_SKILLS      = ["leadership", "communication", "analytical", "creativity",
                     "teamwork", "problemsolving", "sales", "detail"]
WORK_PREFS       = ["remote", "hybrid", "office"]
INDUSTRIES       = ["tech", "finance", "healthcare", "ecommerce", "media", "gov",
                     "consulting", "open"]
SALARY_OPTS      = ["high", "balanced", "impact"]

class FeatureEngineer:
    """Converts raw profile dicts into a numeric feature matrix."""

    def __init__(self):
        self.edu_encoder   = LabelEncoder()
        self.field_encoder = LabelEncoder()
        self.work_encoder  = LabelEncoder()
        self.ind_encoder   = LabelEncoder()
        self.sal_encoder   = LabelEncoder()
        self.tech_mlb      = MultiLabelBinarizer(classes=TECH_SKILLS)
        self.soft_mlb      = MultiLabelBinarizer(classes=SOFT_SKILLS)
        self.scaler        = StandardScaler()
        self.fitted        = False
    
    def _safe_map(self, series, known_classes, fallback):
        return series.apply(lambda x: x if x in known_classes else fallback)

    def _base_features(self, df: pd.DataFrame) -> np.ndarray:
        # --- SAFE HANDLING OF UNSEEN CATEGORIES ---
        df = df.copy()

        df["education"] = self._safe_map(
            df["education"],
            self.edu_encoder.classes_,
            "bachelor"
        )

        df["field_of_study"] = self._safe_map(
            df["field_of_study"],
            self.field_encoder.classes_,
            "other"
        )

        df["work_pref"] = self._safe_map(
            df["work_pref"],
            self.work_encoder.classes_,
            "hybrid"
        )

        df["industry"] = self._safe_map(
            df["industry"],
            self.ind_encoder.classes_,
            "open"
        )

        df["salary_priority"] = self._safe_map(
            df["salary_priority"],
            self.sal_encoder.classes_,
            "balanced"
        )
        edu   = self.edu_encoder.transform(df["education"])
        field = self.field_encoder.transform(df["field_of_study"])
        work  = self.work_encoder.transform(df["work_pref"])
        ind   = self.ind_encoder.transform(df["industry"])
        sal   = self.sal_encoder.transform(df["salary_priority"])
        exp   = df["years_experience"].values.reshape(-1, 1)

        tech_mat = self.tech_mlb.transform(df["tech_skills"])
        soft_mat = self.soft_mlb.transform(df["soft_skills"])

        cats = np.column_stack([edu, field, work, ind, sal])
        return np.hstack([cats, exp, tech_mat, soft_mat])

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        self.edu_encoder.fit(EDUCATION_LEVELS)
        self.field_encoder.fit(FIELDS_OF_STUDY)
        self.work_encoder.fit(WORK_PREFS)
        self.ind_encoder.fit(INDUSTRIES)
        self.sal_encoder.fit(SALARY_OPTS)
        self.tech_mlb.fit([TECH_SKILLS])
        self.soft_mlb.fit([SOFT_SKILLS])
        self.fitted = True

        X = self._base_features(df)
        X[:, 5:6] = self.scaler.fit_transform(X[:, 5:6])  # scale experience only
        return X

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        assert self.fitted, "Call fit_transform first."
        X = self._base_features(df)
        X[:, 5:6] = self.scaler.transform(X[:, 5:6])
        return X

    def transform_single(self, profile: dict) -> np.ndarray:
        """Transform one profile dict (from API request) into a feature row."""
        # Convert list fields stored as JSON strings if needed
        tech = profile.get("tech_skills", [])
        soft = profile.get("soft_skills", [])
        if isinstance(tech, str):
            tech = json.loads(tech)
        if isinstance(soft, str):
            soft = json.loads(soft)

        row = pd.DataFrame([{
            "education":        profile.get("education", "bachelor"),
            "field_of_study":   profile.get("field_of_study", "other"),
            "years_experience": float(profile.get("years_experience", 0)),
            "tech_skills":      tech,
            "soft_skills":      soft,
            "work_pref":        profile.get("work_pref", "hybrid"),
            "industry":         profile.get("industry", "open"),
            "salary_priority":  profile.get("salary_priority", "balanced"),
        }])
        return self.transform(row)