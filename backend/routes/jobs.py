from fastapi import APIRouter

router = APIRouter()


# =========================================================
# JOB DATABASE
# =========================================================

JOB_ROLES = [

    {
        "title": "Python Developer",
        "required_skills": [
            "Python",
            "FastAPI",
            "Flask",
            "SQL",
            "Git",
            "Docker",
            "AWS"
        ],
        "description": "Develop Python applications, APIs and backend services."
    },

    {
        "title": "Full Stack Developer",
        "required_skills": [
            "Python",
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "SQL",
            "Git"
        ],
        "description": "Build frontend and backend web applications."
    },

    {
        "title": "Backend Developer",
        "required_skills": [
            "Python",
            "FastAPI",
            "Flask",
            "SQL",
            "MongoDB",
            "Git",
            "Docker"
        ],
        "description": "Build APIs, backend services and database integrations."
    },

    {
        "title": "Frontend Developer",
        "required_skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ],
        "description": "Build responsive and interactive web interfaces."
    },

    {
        "title": "Data Analyst",
        "required_skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "Excel",
            "Power BI"
        ],
        "description": "Analyze data and create useful business insights."
    },

    {
        "title": "Machine Learning Engineer",
        "required_skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "TensorFlow",
            "Scikit-learn"
        ],
        "description": "Develop and deploy machine learning solutions."
    },

    {
        "title": "Cloud Developer",
        "required_skills": [
            "Python",
            "AWS",
            "Docker",
            "Git",
            "SQL"
        ],
        "description": "Develop and deploy applications using cloud services."
    }
]


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    return skill.strip().lower()


# =========================================================
# RECOMMEND JOBS
# =========================================================

@router.post("/recommend-jobs")
async def recommend_jobs(data: dict):

    resume_skills = data.get(
        "resume_skills",
        []
    )


    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    if not isinstance(resume_skills, list):

        resume_skills = []


    # -----------------------------------------------------
    # Normalize resume skills
    # -----------------------------------------------------

    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }


    recommendations = []


    # -----------------------------------------------------
    # Compare every job
    # -----------------------------------------------------

    for job in JOB_ROLES:

        required_skills = job["required_skills"]


        matched_skills = []

        missing_skills = []


        # -------------------------------------------------
        # Find matched and missing skills
        # -------------------------------------------------

        for skill in required_skills:

            if normalize_skill(skill) in resume_skill_set:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)


        # -------------------------------------------------
        # Calculate percentage
        # -------------------------------------------------

        if len(required_skills) > 0:

            match_percentage = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            match_percentage = 0


        # -------------------------------------------------
        # Add recommendation
        # -------------------------------------------------

        recommendations.append({

            "title": job["title"],

            "description": job["description"],

            "match_percentage": round(
                match_percentage,
                2
            ),

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "total_required_skills": len(
                required_skills
            ),

            "total_matched_skills": len(
                matched_skills
            ),

            "total_missing_skills": len(
                missing_skills
            )
        })


    # -----------------------------------------------------
    # Sort by match percentage
    # -----------------------------------------------------

    recommendations.sort(
        key=lambda job: job["match_percentage"],
        reverse=True
    )


    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {

        "success": True,

        "resume_skills": resume_skills,

        "total_jobs_analyzed": len(
            recommendations
        ),

        "recommendations": recommendations
    }