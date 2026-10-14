# =========================================================
# ANALYSIS ROUTES
# AI JOB SKILL ANALYZER
# =========================================================

from fastapi import APIRouter, UploadFile, File, Form

from services.skill_extractor import (
    extract_skills,
    SKILL_ALIASES
)

from services.pdf_parser import extract_text_from_pdf

import os
import shutil


router = APIRouter()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_skill(skill):
    """
    Convert a skill into a common/canonical format
    for accurate comparison.
    """

    if not skill:
        return ""

    skill = skill.strip().lower()

    # -----------------------------------------------------
    # Direct alias check
    # -----------------------------------------------------

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill].strip().lower()

    # -----------------------------------------------------
    # Normalize separators
    # -----------------------------------------------------

    skill = skill.replace("-", " ")
    skill = skill.replace("_", " ")

    # Remove extra spaces
    skill = " ".join(skill.split())

    # -----------------------------------------------------
    # Check aliases after normalization
    # -----------------------------------------------------

    for alias, main_skill in SKILL_ALIASES.items():

        normalized_alias = alias.lower()

        normalized_alias = normalized_alias.replace("-", " ")
        normalized_alias = normalized_alias.replace("_", " ")

        normalized_alias = " ".join(
            normalized_alias.split()
        )

        if skill == normalized_alias:

            return main_skill.strip().lower()

    return skill


# =========================================================
# CANONICAL SKILL MAP
# =========================================================

SKILL_CANONICAL_MAP = {

    # Programming
    "python3": "python",
    "python": "python",

    "javascript": "javascript",
    "js": "javascript",

    "java": "java",

    "c++": "c++",
    "cpp": "c++",

    "c#": "c#",
    "csharp": "c#",

    # Frontend
    "html5": "html",
    "html": "html",

    "css3": "css",
    "css": "css",

    "react.js": "react",
    "reactjs": "react",
    "react": "react",

    "vue": "vue.js",
    "vuejs": "vue.js",
    "vue.js": "vue.js",

    "angular": "angular",

    "tailwind": "tailwind css",
    "tailwind css": "tailwind css",

    "bootstrap": "bootstrap",

    # Backend
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",

    "express": "express",
    "express.js": "express",

    "fast api": "fastapi",
    "fastapi": "fastapi",

    "flask": "flask",

    "django": "django",

    "rest api": "rest api",
    "restful api": "rest api",

    # Database
    "sql": "sql",
    "mysql": "mysql",

    "mongo db": "mongodb",
    "mongodb": "mongodb",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "sqlite": "sqlite",

    "firebase": "firebase",

    "nosql": "nosql",

    # Cloud
    "aws": "aws",
    "amazon web services": "aws",

    "azure": "azure",

    "google cloud": "google cloud",
    "google cloud platform": "google cloud",

    "gcp": "google cloud",

    # Tools
    "git": "git",
    "github": "github",

    "docker": "docker",

    "kubernetes": "kubernetes",

    "jenkins": "jenkins",

    "ci/cd": "ci/cd",

    # AI / ML
    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",

    "machine learning": "machine learning",
    "ml": "machine learning",

    "deep learning": "deep learning",
    "dl": "deep learning",

    "tensorflow": "tensorflow",
    "keras": "keras",
    "pytorch": "pytorch",

    "scikit-learn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "cnn": "cnn",

    "nlp": "nlp",

    "computer vision": "computer vision",
    "cv": "computer vision",

    "opencv": "opencv",

    # Data Science
    "pandas": "pandas",
    "numpy": "numpy",

    "matplotlib": "matplotlib",
    "seaborn": "seaborn",

    "power bi": "power bi",
    "powerbi": "power bi",

    "tableau": "tableau",

    "excel": "excel",
    "ms excel": "excel",
    "microsoft excel": "excel",

    "word": "word",
    "ms word": "word",
    "microsoft word": "word",

    "big data": "big data",

    "hadoop": "hadoop",

    "mapreduce": "mapreduce",

    # BPO / Customer Support / Business
    "communication skills": "communication skills",
    "communication": "communication skills",
    "english": "english",
    "english communication": "english communication",
    "customer service": "customer service",
    "customer support": "customer support",
    "problem solving": "problem solving",
    "active listening": "active listening",
    "word": "word",
    "ms word": "word",
    "microsoft word": "word",
    "email communication": "email communication",
    "email support": "email support",
    "data entry": "data entry",
    "basic computer skills": "basic computer skills",
    "computer skills": "computer skills",
    "time management": "time management",
    "teamwork": "teamwork",
    "customer relationship management": "customer relationship management",
    "crm": "customer relationship management",
    "typing skills": "typing skills",
    "typing": "typing",
    "voice process": "voice process",
    "non voice process": "non-voice process",
    "non-voice process": "non-voice process",
    "chat support": "chat support",
    "bpo": "bpo",
    "back office": "back office",
    "process associate": "process associate",
    "sales": "sales",
    "negotiation": "negotiation",
    "presentation skills": "presentation skills",
    "leadership": "leadership",
    "adaptability": "adaptability",
    "attention to detail": "attention to detail"
}


# =========================================================
# DISPLAY NAMES
# =========================================================

SKILL_DISPLAY_MAP = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "c": "C",
    "c++": "C++",
    "c#": "C#",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "vue.js": "Vue.js",
    "angular": "Angular",
    "tailwind css": "Tailwind CSS",
    "bootstrap": "Bootstrap",
    "node.js": "Node.js",
    "express": "Express",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "rest api": "REST API",
    "sql": "SQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "postgresql": "PostgreSQL",
    "sqlite": "SQLite",
    "firebase": "Firebase",
    "nosql": "NoSQL",
    "aws": "AWS",
    "azure": "Azure",
    "google cloud": "Google Cloud",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "jenkins": "Jenkins",
    "ci/cd": "CI/CD",
    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "cnn": "CNN",
    "nlp": "NLP",
    "computer vision": "Computer Vision",
    "opencv": "OpenCV",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "excel": "Excel",
    "word": "Word",
    "big data": "Big Data",
    "hadoop": "Hadoop",
    "mapreduce": "MapReduce",

    "communication skills": "Communication Skills",
    "english": "English",
    "english communication": "English Communication",
    "customer service": "Customer Service",
    "customer support": "Customer Support",
    "problem solving": "Problem Solving",
    "active listening": "Active Listening",
    "word": "Word",
    "email communication": "Email Communication",
    "email support": "Email Support",
    "data entry": "Data Entry",
    "basic computer skills": "Basic Computer Skills",
    "computer skills": "Computer Skills",
    "time management": "Time Management",
    "teamwork": "Teamwork",
    "customer relationship management": "Customer Relationship Management",
    "typing skills": "Typing Skills",
    "typing": "Typing",
    "voice process": "Voice Process",
    "non-voice process": "Non-Voice Process",
    "chat support": "Chat Support",
    "bpo": "BPO",
    "back office": "Back Office",
    "process associate": "Process Associate",
    "sales": "Sales",
    "negotiation": "Negotiation",
    "presentation skills": "Presentation Skills",
    "leadership": "Leadership",
    "adaptability": "Adaptability",
    "attention to detail": "Attention to Detail",
}


def display_skill(skill):
    """
    Convert any skill variant into the UI-friendly canonical name.
    """
    canonical = canonical_skill(skill)
    return SKILL_DISPLAY_MAP.get(canonical, canonical)




# =========================================================
# NORMALIZE USING CANONICAL MAP
# =========================================================

def canonical_skill(skill):
    """
    Convert a skill to its final canonical name.
    """

    normalized = normalize_skill(skill)

    if not normalized:
        return ""

    if normalized in SKILL_CANONICAL_MAP:

        return SKILL_CANONICAL_MAP[
            normalized
        ]

    return normalized


# =========================================================
# REMOVE DUPLICATE SKILLS
# =========================================================

def unique_skills(skills):
    """
    Remove duplicate skills while preserving order.
    Always return UI-friendly canonical names.
    """

    result = []
    seen = set()

    for skill in skills:

        canonical = canonical_skill(skill)

        if not canonical:
            continue

        if canonical not in seen:
            result.append(display_skill(canonical))
            seen.add(canonical)

    return result


# =========================================================
# CALCULATE SKILL MATCH
# =========================================================

def calculate_skill_match(
    resume_skills,
    required_skills
):
    """
    Compare resume skills with required job skills.

    The comparison is:
    - case-insensitive
    - alias-aware
    - separator-aware
    - duplicate-safe
    - canonicalized before calculating the percentage

    Example:
        Excel == MS Excel == Microsoft Excel
        React == React.js == ReactJS
        FastAPI == Fast API
        MongoDB == Mongo DB
    """

    # -----------------------------------------------------
    # Extra aliases used specifically for reliable matching
    # -----------------------------------------------------

    EXTRA_MATCH_ALIASES = {
        "ms excel": "excel",
        "microsoft excel": "excel",
        "ms-excel": "excel",

        "ms word": "word",
        "microsoft word": "word",
        "ms-word": "word",

        "react.js": "react",
        "react js": "react",
        "reactjs": "react",

        "fast api": "fastapi",
        "fast-api": "fastapi",

        "mongo db": "mongodb",
        "mongo-db": "mongodb",

        "node": "node.js",
        "nodejs": "node.js",

        "powerbi": "power bi",
        "power-bi": "power bi",

        "google cloud platform": "google cloud",
        "gcp": "google cloud",

        "machine learning": "machine learning",
        "ml": "machine learning",

        "artificial intelligence": "artificial intelligence",
        "ai": "artificial intelligence",

        # BPO / Customer Support
        "communication": "communication skills",
        "communication skill": "communication skills",
        "communication skills": "communication skills",
        "english communication": "english communication",
        "customer service": "customer service",
        "customer support": "customer support",
        "problem solving": "problem solving",
        "active listening": "active listening",
        "ms excel": "excel",
        "microsoft excel": "excel",
        "ms word": "word",
        "microsoft word": "word",
        "email communication": "email communication",
        "email support": "email support",
        "data entry": "data entry",
        "basic computer skills": "basic computer skills",
        "computer skills": "computer skills",
        "time management": "time management",
        "teamwork": "teamwork",
        "customer relationship management": "customer relationship management",
        "crm": "customer relationship management",
        "typing skills": "typing skills",
        "typing": "typing",
        "voice process": "voice process",
        "non voice process": "non-voice process",
        "non-voice process": "non-voice process",
        "chat support": "chat support",
        "back office": "back office",
        "process associate": "process associate",
    }

    def match_canonical_skill(skill):
        """
        Return one canonical value for comparison only.
        """

        if skill is None:
            return ""

        value = str(skill).strip().lower()

        if not value:
            return ""

        # Normalize separators and whitespace.
        value = value.replace("_", " ")
        value = value.replace("-", " ")
        value = " ".join(value.split())

        # Direct extra alias.
        if value in EXTRA_MATCH_ALIASES:
            value = EXTRA_MATCH_ALIASES[value]

        # Existing project alias system.
        if value in SKILL_ALIASES:
            value = SKILL_ALIASES[value].strip().lower()
            value = value.replace("_", " ")
            value = value.replace("-", " ")
            value = " ".join(value.split())

        # Existing canonical map.
        if value in SKILL_CANONICAL_MAP:
            return SKILL_CANONICAL_MAP[value]

        # Handle aliases after normalization.
        for alias, main_skill in SKILL_ALIASES.items():

            alias_normalized = str(alias).strip().lower()
            alias_normalized = alias_normalized.replace("_", " ")
            alias_normalized = alias_normalized.replace("-", " ")
            alias_normalized = " ".join(alias_normalized.split())

            if value == alias_normalized:
                main = str(main_skill).strip().lower()
                main = main.replace("_", " ")
                main = main.replace("-", " ")
                main = " ".join(main.split())

                return SKILL_CANONICAL_MAP.get(main, main)

        return value

    # -----------------------------------------------------
    # Build canonical resume skill set
    # -----------------------------------------------------

    resume_set = set()

    for skill in resume_skills or []:

        canonical = match_canonical_skill(skill)

        if canonical:
            resume_set.add(canonical)

    # -----------------------------------------------------
    # Build unique canonical required skills
    # -----------------------------------------------------

    required_items = []
    required_seen = set()

    for skill in required_skills or []:

        canonical = match_canonical_skill(skill)

        if not canonical:
            continue

        if canonical not in required_seen:

            required_items.append(
                (canonical, display_skill(canonical))
            )

            required_seen.add(canonical)

    # -----------------------------------------------------
    # Compare resume vs job requirements
    # -----------------------------------------------------

    matched_skills = []
    missing_skills = []

    for canonical, display_name in required_items:

        if canonical in resume_set:
            matched_skills.append(display_name)
        else:
            missing_skills.append(display_name)

    # -----------------------------------------------------
    # Remove duplicates from final output
    # -----------------------------------------------------

    matched_skills = list(dict.fromkeys(matched_skills))
    missing_skills = list(dict.fromkeys(missing_skills))

    # -----------------------------------------------------
    # Calculate percentage using canonical required count
    # -----------------------------------------------------

    total_required = len(required_items)
    total_matched = len(matched_skills)

    if total_required > 0:
        match_percentage = (
            total_matched / total_required
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
    # Get frontend data
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
    # Safety checks
    # -----------------------------------------------------

    if not isinstance(
        resume_skills,
        list
    ):

        resume_skills = []

    if not isinstance(
        job_description,
        str
    ):

        job_description = ""

    # -----------------------------------------------------
    # Extract required skills from JD
    # -----------------------------------------------------

    required_skills = extract_skills(
        job_description
    )

    # -----------------------------------------------------
    # Calculate match
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

    resume_skills = unique_skills(resume_skills)
    required_skills = unique_skills(required_skills)

    return {

        "success": True,

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_percentage": match_percentage,

        "total_required_skills": len(
            required_skills
        ),

        "total_matched_skills": len(
            matched_skills
        ),

        "total_missing_skills": len(
            missing_skills
        )
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

            "message":
                "No resume file provided"
        }

    # -----------------------------------------------------
    # Validate PDF
    # -----------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        return {

            "success": False,

            "message":
                "Only PDF resumes are supported"
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
    # Canonicalize extracted skills before comparison
    # -----------------------------------------------------

    resume_skills = unique_skills(resume_skills)
    required_skills = unique_skills(required_skills)

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

        "filename":
            file.filename,

        "resume_text":
            resume_text,

        "resume_skills":
            resume_skills,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "match_percentage":
            match_percentage,

        "total_required_skills":
            len(required_skills),

        "total_matched_skills":
            len(matched_skills),

        "total_missing_skills":
            len(missing_skills)
    }


# =========================================================
# 3. LEARNING ROADMAP
# =========================================================

ROADMAP = {

    # -----------------------------------------------------
    # Frontend
    # -----------------------------------------------------

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

        "resource":
            "https://react.dev/learn",

        "project":
            "Build a React Job Portal"
    },

    # -----------------------------------------------------
    # Backend
    # -----------------------------------------------------

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

        "resource":
            "https://fastapi.tiangolo.com/tutorial/",

        "project":
            "Build a Resume Analysis API"
    },

    "Python": {

        "level": "Beginner",

        "duration": "10 Days",

        "topics": [
            "Python fundamentals",
            "Functions and modules",
            "Lists, tuples and dictionaries",
            "Object-oriented programming",
            "File handling",
            "Build a Python project"
        ],

        "resource":
            "https://docs.python.org/3/tutorial/",

        "project":
            "Build a Python Job Tracker"
    },

    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------

    "SQL": {

        "level": "Beginner",

        "duration": "7 Days",

        "topics": [
            "SQL fundamentals",
            "SELECT and WHERE",
            "JOIN operations",
            "GROUP BY and aggregate functions",
            "Subqueries",
            "Build a database project"
        ],

        "resource":
            "https://www.w3schools.com/sql/",

        "project":
            "Build an Employee Management Database"
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

        "resource":
            "https://www.mongodb.com/docs/manual/",

        "project":
            "Build a Student Management API"
    },

    # -----------------------------------------------------
    # DevOps
    # -----------------------------------------------------

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

        "resource":
            "https://docs.docker.com/get-started/",

        "project":
            "Dockerize a FastAPI Application"
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

        "resource":
            "https://git-scm.com/docs/gittutorial",

        "project":
            "Publish a Project on GitHub"
    },

    "GitHub": {

        "level": "Beginner",

        "duration": "3 Days",

        "topics": [
            "GitHub fundamentals",
            "Repositories",
            "Push projects",
            "Branches",
            "Pull requests"
        ],

        "resource":
            "https://docs.github.com/en/get-started",

        "project":
            "Publish Your Portfolio Project on GitHub"
    },

    # -----------------------------------------------------
    # Cloud
    # -----------------------------------------------------

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

        "resource":
            "https://aws.amazon.com/getting-started/",

        "project":
            "Deploy a Web Application on AWS"
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

    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    if not isinstance(
        missing_skills,
        list
    ):

        missing_skills = []

    roadmap = {}

    # -----------------------------------------------------
    # Find roadmap for each missing skill
    # -----------------------------------------------------

    for skill in missing_skills:

        if not skill:
            continue

        # Direct match
        if skill in ROADMAP:

            roadmap[skill] = ROADMAP[skill]

            continue

        # Case-insensitive match
        for roadmap_skill in ROADMAP:

            if (
                skill.lower()
                == roadmap_skill.lower()
            ):

                roadmap[roadmap_skill] = (
                    ROADMAP[roadmap_skill]
                )

                break

    # -----------------------------------------------------
    # Return roadmap
    # -----------------------------------------------------

    return {

        "success": True,

        "missing_skills":
            missing_skills,

        "roadmap":
            roadmap
    }