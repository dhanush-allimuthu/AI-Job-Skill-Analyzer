from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os
import re

from services.pdf_parser import extract_text_from_pdf

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# CANONICAL SKILL DATABASE
# =========================================================

SKILL_DATABASE = {
    "Programming Languages": [
        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#"
    ],

    "Frontend": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Vue.js",
        "Tailwind CSS",
        "Bootstrap"
    ],

    "Backend": [
        "Node.js",
        "Express",
        "FastAPI",
        "Flask",
        "Django",
        "REST API"
    ],

    "Database": [
        "SQL",
        "MySQL",
        "MongoDB",
        "PostgreSQL",
        "Firebase",
        "SQLite",
        "NoSQL"
    ],

    "Cloud": [
        "AWS",
        "Azure",
        "Google Cloud"
    ],

    "DevOps": [
        "Git",
        "GitHub",
        "Docker",
        "Kubernetes",
        "Jenkins",
        "CI/CD"
    ],

    "AI / Machine Learning": [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "Scikit-learn",
        "CNN",
        "NLP",
        "Computer Vision",
        "OpenCV"
    ],

    "Data Science": [
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Power BI",
        "Tableau",
        "Excel",
        "Big Data",
        "Hadoop",
        "MapReduce"
    ]
}


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {
    "python3": "Python",

    "js": "JavaScript",
    "ecmascript": "JavaScript",

    "html5": "HTML",

    "css3": "CSS",

    "react.js": "React",
    "reactjs": "React",

    "vue": "Vue.js",
    "vuejs": "Vue.js",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "express.js": "Express",
    "expressjs": "Express",

    "fast api": "FastAPI",

    "restful api": "REST API",

    "mongo db": "MongoDB",
    "mongodb": "MongoDB",

    "postgres": "PostgreSQL",

    "amazon web services": "AWS",

    "google cloud platform": "Google Cloud",
    "gcp": "Google Cloud",

    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "powerbi": "Power BI",
    "power-bi": "Power BI"
}


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for case-insensitive skill matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    # Keep dots for aliases such as react.js / node.js.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill_key(skill: str) -> str:
    """
    Create a comparison key for canonical skills.
    """

    normalized = normalize_text(skill)

    # Treat punctuation variants as the same skill.
    normalized = normalized.replace(".", "")
    normalized = normalized.replace(" ", "")

    return normalized


# =========================================================
# CANONICAL MAP
# =========================================================

def build_canonical_map():
    mapping = {}

    for skills in SKILL_DATABASE.values():
        for skill in skills:
            mapping[normalize_skill_key(skill)] = skill

    for alias, canonical in SKILL_ALIASES.items():
        mapping[normalize_skill_key(alias)] = canonical

    return mapping


CANONICAL_MAP = build_canonical_map()


# =========================================================
# SKILL MATCHING
# =========================================================

def skill_exists(text: str, skill: str) -> bool:
    """
    Case-insensitive exact word/phrase matching.
    """

    normalized_text = normalize_text(text)
    normalized_skill = normalize_text(skill)

    if not normalized_text or not normalized_skill:
        return False

    # C / C++ / C# need special handling.
    if normalized_skill in {"c", "c++", "c#"}:
        return re.search(
            r"(?<!\w)" + re.escape(normalized_skill) + r"(?!\w)",
            normalized_text
        ) is not None

    # General word/phrase matching.
    return re.search(
        r"(?<!\w)" + re.escape(normalized_skill) + r"(?!\w)",
        normalized_text
    ) is not None


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills_from_text(text: str):
    """
    Return only unique canonical skill names.

    Example:
        HTML + HTML5 -> HTML
        React + React.js -> React
        Node.js + nodejs -> Node.js
    """

    detected_skills = []
    categorized_skills = {}
    seen = set()

    normalized_text = normalize_text(text)

    def add_skill(canonical_skill: str, category: str):
        key = normalize_skill_key(canonical_skill)

        if key not in seen:
            detected_skills.append(canonical_skill)
            seen.add(key)

        if category not in categorized_skills:
            categorized_skills[category] = []

        if canonical_skill not in categorized_skills[category]:
            categorized_skills[category].append(canonical_skill)

    # -----------------------------------------------------
    # Check canonical skills
    # -----------------------------------------------------

    for category, skills in SKILL_DATABASE.items():

        for skill in skills:

            if skill_exists(normalized_text, skill):
                add_skill(skill, category)

    # -----------------------------------------------------
    # Check aliases
    # -----------------------------------------------------

    alias_to_category = {}

    for category, skills in SKILL_DATABASE.items():
        for skill in skills:
            alias_to_category[skill] = category

    for alias, canonical in SKILL_ALIASES.items():

        if skill_exists(normalized_text, alias):

            category = alias_to_category.get(
                canonical,
                "Other"
            )

            add_skill(canonical, category)

    return detected_skills, categorized_skills


# =========================================================
# REQUEST MODEL
# =========================================================

class SkillExtractionRequest(BaseModel):
    resume_text: str


# =========================================================
# UPLOAD RESUME
# =========================================================

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename:
        return {
            "success": False,
            "message": "No file selected"
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF resume files are supported"
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text_from_pdf(file_path)

    skills, categorized_skills = extract_skills_from_text(text)

    return {
        "success": True,
        "filename": file.filename,
        "message": "Resume uploaded successfully",
        "extracted_text": text,
        "skills": skills,
        "categorized_skills": categorized_skills,
        "total_skills": len(skills)
    }


# =========================================================
# EXTRACT SKILLS API
# =========================================================

@router.post("/extract-skills")
async def extract_skills(request: SkillExtractionRequest):

    text = request.resume_text

    if not text or not text.strip():
        return {
            "success": False,
            "message": "Resume text is empty",
            "skills": [],
            "categorized_skills": {},
            "total_skills": 0
        }

    skills, categorized_skills = extract_skills_from_text(text)

    return {
        "success": True,
        "message": "Skills extracted successfully",
        "skills": skills,
        "categorized_skills": categorized_skills,
        "total_skills": len(skills)
    }
