from fastapi import APIRouter, UploadFile, File, Form

from services.skill_extractor import extract_skills
from services.pdf_parser import extract_text_from_pdf

import os
import shutil


router = APIRouter()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_skill(skill):
    """
    Normalize skill names for comparison.
    """

    return skill.strip().lower()


def calculate_skill_match(resume_skills, required_skills):
    """
    Compare resume skills with required job skills.
    """

    resume_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        normalized = normalize_skill(skill)

        if normalized in resume_set:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)


    # -----------------------------------------------------
    # Match Percentage
    # -----------------------------------------------------

    if len(required_skills) > 0:

        match_percentage = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        match_percentage = 0


    return (
        matched_skills,
        missing_skills,
        round(match_percentage, 2)
    )


# =========================================================
# 1. SKILL GAP ANALYSIS
# =========================================================

@router.post("/skill-gap")
async def skill_gap_analysis(data: dict):

    # -----------------------------------------------------
    # Get data from frontend
    # -----------------------------------------------------

    resume_skills = data.get(
        "resume_skills",
        []
    )

    job_description = data.get(
        "job_description",
        ""
    )


    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    if not isinstance(resume_skills, list):

        resume_skills = []


    # -----------------------------------------------------
    # Extract required skills from JD
    # -----------------------------------------------------

    required_skills = extract_skills(
        job_description
    )


    # -----------------------------------------------------
    # Compare skills
    # -----------------------------------------------------

    (
        matched_skills,
        missing_skills,
        match_percentage
    ) = calculate_skill_match(
        resume_skills,
        required_skills
    )


    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_percentage": match_percentage
    }


# =========================================================
# 2. COMPLETE RESUME ANALYSIS
# =========================================================

@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # -----------------------------------------------------
    # Upload folder
    # -----------------------------------------------------

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    # -----------------------------------------------------
    # Validate filename
    # -----------------------------------------------------

    if not file.filename:

        return {
            "success": False,
            "message": "No resume file provided"
        }


    # -----------------------------------------------------
    # Create file path
    # -----------------------------------------------------

    file_path = os.path.join(
        upload_folder,
        file.filename
    )


    # -----------------------------------------------------
    # Save uploaded PDF
    # -----------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # -----------------------------------------------------
    # Extract resume text
    # -----------------------------------------------------

    resume_text = extract_text_from_pdf(
        file_path
    )


    # -----------------------------------------------------
    # Extract resume skills
    # -----------------------------------------------------

    resume_skills = extract_skills(
        resume_text
    )


    # -----------------------------------------------------
    # Extract required skills from JD
    # -----------------------------------------------------

    required_skills = extract_skills(
        job_description
    )


    # -----------------------------------------------------
    # Calculate skill match
    # -----------------------------------------------------

    (
        matched_skills,
        missing_skills,
        match_percentage
    ) = calculate_skill_match(
        resume_skills,
        required_skills
    )


    # -----------------------------------------------------
    # Return complete analysis
    # -----------------------------------------------------

    return {

        "success": True,

        "filename": file.filename,

        "resume_text": resume_text,

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_percentage": match_percentage
    }


# =========================================================
# 3. LEARNING ROADMAP
# =========================================================

ROADMAP = {

    "React": {

        "level": "Beginner",

        "duration": "7 Days",

        "topics": [
            "React fundamentals",
            "Components and props",
            "State and events",
            "React Router",
            "Build a React project"
        ],

        "resource": "https://react.dev/learn",

        "project": "Build a React Job Portal"
    },


    "FastAPI": {

        "level": "Beginner",

        "duration": "5 Days",

        "topics": [
            "FastAPI fundamentals",
            "REST API concepts",
            "Request and response handling",
            "Authentication and validation",
            "Build a FastAPI project"
        ],

        "resource": "https://fastapi.tiangolo.com/tutorial/",

        "project": "Build a Resume Analysis API"
    },


    "SQL": {

        "level": "Beginner",

        "duration": "7 Days",

        "topics": [
            "SQL fundamentals",
            "SELECT and WHERE",
            "JOIN operations",
            "GROUP BY and aggregate functions",
            "Build a database project"
        ],

        "resource": "https://www.w3schools.com/sql/",

        "project": "Build an Employee Management Database"
    },


    "Docker": {

        "level": "Beginner",

        "duration": "5 Days",

        "topics": [
            "Docker fundamentals",
            "Images and containers",
            "Dockerfile",
            "Docker Compose",
            "Containerize a web application"
        ],

        "resource": "https://docs.docker.com/get-started/",

        "project": "Dockerize a FastAPI Application"
    },


    "AWS": {

        "level": "Beginner",

        "duration": "10 Days",

        "topics": [
            "AWS fundamentals",
            "EC2",
            "S3",
            "IAM",
            "Deploy a web application"
        ],

        "resource": "https://aws.amazon.com/getting-started/",

        "project": "Deploy a Web Application on AWS"
    },


    "MongoDB": {

        "level": "Beginner",

        "duration": "5 Days",

        "topics": [
            "MongoDB fundamentals",
            "Collections and documents",
            "CRUD operations",
            "Queries and filters",
            "Connect MongoDB with Python"
        ],

        "resource": "https://www.mongodb.com/docs/manual/",

        "project": "Build a Student Management API"
    },


    "Git": {

        "level": "Beginner",

        "duration": "3 Days",

        "topics": [
            "Git fundamentals",
            "Repositories",
            "Commit and push",
            "Branches",
            "Pull requests"
        ],

        "resource": "https://git-scm.com/docs/gittutorial",

        "project": "Publish a Project on GitHub"
    }
}


# =========================================================
# 4. LEARNING ROADMAP API
# =========================================================

@router.post("/learning-roadmap")
def learning_roadmap(data: dict):

    missing_skills = data.get(
        "missing_skills",
        []
    )

    roadmap = {}


    for skill in missing_skills:

        # Direct match
        if skill in ROADMAP:

            roadmap[skill] = ROADMAP[skill]

            continue


        # Case-insensitive match
        for roadmap_skill in ROADMAP:

            if skill.lower() == roadmap_skill.lower():

                roadmap[roadmap_skill] = ROADMAP[
                    roadmap_skill
                ]

                break


    return {

        "missing_skills": missing_skills,

        "roadmap": roadmap
    }