from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os
import re

from services.pdf_parser import extract_text_from_pdf


router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# SKILL DATABASE
# =========================================================

SKILL_DATABASE = {

    "Programming Languages": [
        "python",
        "java",
        "javascript",
        "c",
        "c++",
        "c#"
    ],

    "Frontend": [
        "html",
        "html5",
        "css",
        "css3",
        "javascript",
        "react",
        "react.js",
        "vue",
        "vue.js",
        "tailwind",
        "bootstrap"
    ],

    "Backend": [
        "flask",
        "fastapi",
        "django",
        "node.js",
        "nodejs",
        "express",
        "express.js",
        "rest api",
        "restful api"
    ],

    "Database": [
        "sql",
        "mysql",
        "mongodb",
        "postgresql",
        "firebase",
        "sqlite",
        "nosql"
    ],

    "Cloud": [
        "aws",
        "amazon web services",
        "azure",
        "google cloud",
        "gcp"
    ],

    "DevOps": [
        "git",
        "github",
        "docker",
        "kubernetes",
        "jenkins",
        "ci/cd"
    ],

    "AI / Machine Learning": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "keras",
        "pytorch",
        "scikit-learn",
        "sklearn",
        "cnn",
        "nlp",
        "computer vision",
        "opencv"
    ],

    "Data Science": [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "power bi",
        "tableau",
        "excel",
        "big data",
        "hadoop",
        "mapreduce"
    ]
}


# =========================================================
# REQUEST MODEL
# =========================================================

class SkillExtractionRequest(BaseModel):
    resume_text: str


# =========================================================
# SKILL MATCHING HELPER
# =========================================================

def skill_exists(text: str, skill: str) -> bool:

    text = text.lower()
    skill = skill.lower()

    # Special handling for C++ and C#
    if skill in ["c++", "c#"]:
        return skill in text

    # Word / phrase matching
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return re.search(pattern, text) is not None


# =========================================================
# EXTRACT SKILLS FROM TEXT
# =========================================================

def extract_skills_from_text(text: str):

    detected_skills = []
    categorized_skills = {}

    for category, skills in SKILL_DATABASE.items():

        category_skills = []

        for skill in skills:

            if skill_exists(text, skill):

                if skill not in detected_skills:
                    detected_skills.append(skill)

                if skill not in category_skills:
                    category_skills.append(skill)

        if category_skills:
            categorized_skills[category] = category_skills

    return detected_skills, categorized_skills


# =========================================================
# UPLOAD RESUME
# =========================================================

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Validate PDF
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Save PDF
    # -----------------------------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        buffer.write(
            await file.read()
        )


    # -----------------------------------------------------
    # Extract text
    # -----------------------------------------------------

    text = extract_text_from_pdf(file_path)


    # -----------------------------------------------------
    # Extract skills
    # -----------------------------------------------------

    skills, categorized_skills = extract_skills_from_text(
        text
    )


    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

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
async def extract_skills(
    request: SkillExtractionRequest
):

    # -----------------------------------------------------
    # Get resume text
    # -----------------------------------------------------

    text = request.resume_text


    # -----------------------------------------------------
    # Validate text
    # -----------------------------------------------------

    if not text or not text.strip():

        return {

            "success": False,

            "message": "Resume text is empty",

            "skills": [],

            "categorized_skills": {},

            "total_skills": 0
        }


    # -----------------------------------------------------
    # Extract skills
    # -----------------------------------------------------

    skills, categorized_skills = extract_skills_from_text(
        text
    )


    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {

        "success": True,

        "message": "Skills extracted successfully",

        "skills": skills,

        "categorized_skills": categorized_skills,

        "total_skills": len(skills)
    }