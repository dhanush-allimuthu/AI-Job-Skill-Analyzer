from fastapi import APIRouter

from services.skill_extractor import SKILL_ALIASES


router = APIRouter()


# =========================================================
# JOB DATABASE
# =========================================================

JOB_ROLES = [{'title': 'Python Developer',
  'required_skills': ['Python', 'FastAPI', 'Flask', 'SQL', 'Git', 'Docker'],
  'category': 'IT & Software',
  'description': 'Develop Python applications, REST APIs and backend services.'},
 {'title': 'Java Developer',
  'required_skills': ['Java', 'SQL', 'Git', 'Spring Boot'],
  'category': 'IT & Software',
  'description': 'Develop Java applications, APIs and enterprise software.'},
 {'title': 'JavaScript Developer',
  'required_skills': ['JavaScript', 'HTML', 'CSS', 'Git', 'REST API'],
  'category': 'IT & Software',
  'description': 'Build JavaScript-based web applications and integrations.'},
 {'title': 'Software Developer',
  'required_skills': ['Python', 'JavaScript', 'Git', 'SQL', 'REST API'],
  'category': 'IT & Software',
  'description': 'Develop, test and maintain software applications.'},
 {'title': 'Software Engineer',
  'required_skills': ['Python', 'Java', 'Git', 'SQL', 'REST API'],
  'category': 'IT & Software',
  'description': 'Design, develop and maintain software solutions.'},
 {'title': 'Full Stack Developer',
  'required_skills': ['Python', 'JavaScript', 'HTML', 'CSS', 'React', 'Node.js', 'SQL', 'Git'],
  'category': 'IT & Software',
  'description': 'Build frontend and backend web applications.'},
 {'title': 'Frontend Developer',
  'required_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Git'],
  'category': 'IT & Software',
  'description': 'Build responsive and interactive web interfaces.'},
 {'title': 'Backend Developer',
  'required_skills': ['Python', 'FastAPI', 'Flask', 'SQL', 'MongoDB', 'Git', 'Docker'],
  'category': 'IT & Software',
  'description': 'Build APIs, backend services and database integrations.'},
 {'title': 'Web Developer',
  'required_skills': ['HTML', 'CSS', 'JavaScript', 'Git', 'REST API'],
  'category': 'IT & Software',
  'description': 'Create and maintain responsive websites and web applications.'},
 {'title': 'React Developer',
  'required_skills': ['JavaScript', 'React', 'HTML', 'CSS', 'Git'],
  'category': 'IT & Software',
  'description': 'Develop modern React-based user interfaces.'},
 {'title': 'Node.js Developer',
  'required_skills': ['JavaScript', 'Node.js', 'Express', 'MongoDB', 'REST API', 'Git'],
  'category': 'IT & Software',
  'description': 'Develop Node.js backend applications and APIs.'},
 {'title': 'API Developer',
  'required_skills': ['Python', 'FastAPI', 'REST API', 'SQL', 'Git'],
  'category': 'IT & Software',
  'description': 'Design and develop REST APIs and service integrations.'},
 {'title': 'Django Developer',
  'required_skills': ['Python', 'Django', 'SQL', 'Git', 'REST API'],
  'category': 'IT & Software',
  'description': 'Develop Django web applications and APIs.'},
 {'title': 'Flask Developer',
  'required_skills': ['Python', 'Flask', 'SQL', 'Git', 'REST API'],
  'category': 'IT & Software',
  'description': 'Develop lightweight Python web applications and APIs.'},
 {'title': 'Mobile App Developer',
  'required_skills': ['Java', 'JavaScript', 'Firebase', 'Git'],
  'category': 'IT & Software',
  'description': 'Develop and maintain mobile applications.'},
 {'title': 'UI Developer',
  'required_skills': ['HTML', 'CSS', 'JavaScript', 'Bootstrap', 'Git'],
  'category': 'IT & Software',
  'description': 'Build user interfaces and responsive web pages.'},
 {'title': 'WordPress Developer',
  'required_skills': ['HTML', 'CSS', 'JavaScript', 'PHP'],
  'category': 'IT & Software',
  'description': 'Create and customize WordPress websites.'},
 {'title': 'Junior Software Developer',
  'required_skills': ['Python', 'JavaScript', 'Git', 'SQL'],
  'category': 'IT & Software',
  'description': 'Support development, testing and maintenance of software projects.'},
 {'title': 'QA Engineer',
  'required_skills': ['Java', 'Selenium', 'Git', 'SQL'],
  'category': 'Testing & QA',
  'description': 'Test applications, identify defects and support software quality.'},
 {'title': 'Software Tester',
  'required_skills': ['Java', 'Selenium', 'SQL', 'Git'],
  'category': 'Testing & QA',
  'description': 'Execute software tests and report application defects.'},
 {'title': 'Automation Tester',
  'required_skills': ['Java', 'Selenium', 'Git', 'SQL'],
  'category': 'Testing & QA',
  'description': 'Create and execute automated software tests.'},
 {'title': 'Manual Tester',
  'required_skills': ['SQL', 'Git'],
  'category': 'Testing & QA',
  'description': 'Perform functional, regression and usability testing.'},
 {'title': 'QA Analyst',
  'required_skills': ['SQL', 'Git', 'Java'],
  'category': 'Testing & QA',
  'description': 'Analyze requirements and validate software quality.'},
 {'title': 'Data Analyst',
  'required_skills': ['Python', 'SQL', 'Pandas', 'NumPy', 'Excel', 'Power BI'],
  'category': 'Data & Analytics',
  'description': 'Analyze data and create useful business insights.'},
 {'title': 'Junior Data Analyst',
  'required_skills': ['Excel', 'SQL', 'Python', 'Pandas'],
  'category': 'Data & Analytics',
  'description': 'Prepare, analyze and report business data.'},
 {'title': 'Business Intelligence Analyst',
  'required_skills': ['SQL', 'Excel', 'Power BI', 'Python'],
  'category': 'Data & Analytics',
  'description': 'Build reports and dashboards for business decision-making.'},
 {'title': 'Data Scientist',
  'required_skills': ['Python', 'SQL', 'Pandas', 'NumPy', 'Machine Learning', 'Scikit-learn'],
  'category': 'Data & Analytics',
  'description': 'Analyze datasets and build predictive models.'},
 {'title': 'Data Engineer',
  'required_skills': ['Python', 'SQL', 'Pandas', 'Big Data', 'Hadoop'],
  'category': 'Data & Analytics',
  'description': 'Build data pipelines and data processing solutions.'},
 {'title': 'Machine Learning Engineer',
  'required_skills': ['Python',
                      'Machine Learning',
                      'Pandas',
                      'NumPy',
                      'TensorFlow',
                      'Scikit-learn'],
  'category': 'AI & ML',
  'description': 'Develop and deploy machine learning solutions.'},
 {'title': 'AI Engineer',
  'required_skills': ['Python', 'Artificial Intelligence', 'Machine Learning', 'TensorFlow', 'Git'],
  'category': 'AI & ML',
  'description': 'Develop AI-based applications and intelligent systems.'},
 {'title': 'Deep Learning Engineer',
  'required_skills': ['Python', 'Deep Learning', 'TensorFlow', 'Keras', 'NumPy'],
  'category': 'AI & ML',
  'description': 'Develop deep learning models and applications.'},
 {'title': 'NLP Engineer',
  'required_skills': ['Python', 'NLP', 'Machine Learning', 'TensorFlow'],
  'category': 'AI & ML',
  'description': 'Build natural language processing solutions.'},
 {'title': 'Computer Vision Engineer',
  'required_skills': ['Python', 'Computer Vision', 'OpenCV', 'TensorFlow', 'NumPy'],
  'category': 'AI & ML',
  'description': 'Develop computer vision and image analysis solutions.'},
 {'title': 'Cloud Developer',
  'required_skills': ['Python', 'AWS', 'Docker', 'Git', 'SQL'],
  'category': 'Cloud & DevOps',
  'description': 'Develop and deploy applications using cloud services.'},
 {'title': 'Cloud Engineer',
  'required_skills': ['AWS', 'Docker', 'Linux', 'Git', 'Kubernetes'],
  'category': 'Cloud & DevOps',
  'description': 'Deploy and maintain cloud infrastructure and applications.'},
 {'title': 'AWS Cloud Engineer',
  'required_skills': ['AWS', 'Docker', 'Git', 'Linux'],
  'category': 'Cloud & DevOps',
  'description': 'Build and support applications on AWS.'},
 {'title': 'DevOps Engineer',
  'required_skills': ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD'],
  'category': 'Cloud & DevOps',
  'description': 'Automate software delivery and infrastructure workflows.'},
 {'title': 'Cloud Support Engineer',
  'required_skills': ['AWS', 'Linux', 'Git', 'Docker'],
  'category': 'Cloud & DevOps',
  'description': 'Support cloud applications, infrastructure and deployments.'},
 {'title': 'System Administrator',
  'required_skills': ['Linux', 'AWS', 'Git'],
  'category': 'IT Support',
  'description': 'Maintain systems, users, servers and IT infrastructure.'},
 {'title': 'Technical Support Engineer',
  'required_skills': ['Python', 'SQL', 'Git'],
  'category': 'IT Support',
  'description': 'Troubleshoot technical issues and support customers or internal users.'},
 {'title': 'IT Support Executive',
  'required_skills': ['Excel', 'Word', 'Problem Solving', 'Communication'],
  'category': 'IT Support',
  'description': 'Provide first-level technical and application support.'},
 {'title': 'Application Support Engineer',
  'required_skills': ['SQL', 'Python', 'Git', 'Problem Solving'],
  'category': 'IT Support',
  'description': 'Monitor applications and troubleshoot production issues.'},
 {'title': 'Customer Support Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Problem Solving', 'Excel'],
  'category': 'BPO & Customer Support',
  'description': 'Handle customer queries through calls, email or chat.'},
 {'title': 'Customer Service Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Problem Solving', 'Excel'],
  'category': 'BPO & Customer Support',
  'description': 'Assist customers and resolve service-related queries.'},
 {'title': 'BPO Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Excel', 'Time Management'],
  'category': 'BPO & Customer Support',
  'description': 'Handle customer interactions and follow process standards.'},
 {'title': 'Voice Process Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Problem Solving'],
  'category': 'BPO & Customer Support',
  'description': 'Handle inbound or outbound customer calls.'},
 {'title': 'Non-Voice Process Executive',
  'required_skills': ['English', 'Email Communication', 'Data Entry', 'Excel'],
  'category': 'BPO & Customer Support',
  'description': 'Process customer requests through email and non-voice channels.'},
 {'title': 'Chat Support Executive',
  'required_skills': ['English', 'Communication', 'Customer Service', 'Typing', 'Problem Solving'],
  'category': 'BPO & Customer Support',
  'description': 'Provide customer support through live chat.'},
 {'title': 'Technical Support Executive',
  'required_skills': ['Communication', 'English', 'Problem Solving', 'Basic Computer Skills'],
  'category': 'BPO & Customer Support',
  'description': 'Provide technical assistance to customers.'},
 {'title': 'Process Associate',
  'required_skills': ['Communication', 'English', 'Excel', 'Data Entry', 'Time Management'],
  'category': 'BPO & Operations',
  'description': 'Process customer or business transactions accurately.'},
 {'title': 'Back Office Executive',
  'required_skills': ['Excel', 'Word', 'Data Entry', 'Communication'],
  'category': 'BPO & Operations',
  'description': 'Handle documentation, data processing and back-office tasks.'},
 {'title': 'Data Entry Operator',
  'required_skills': ['Excel', 'Data Entry', 'Typing', 'Basic Computer Skills'],
  'category': 'BPO & Operations',
  'description': 'Enter, verify and maintain business data.'},
 {'title': 'Business Analyst',
  'required_skills': ['Excel', 'SQL', 'Python', 'Power BI', 'Communication'],
  'category': 'Business & Operations',
  'description': 'Analyze business requirements and support data-driven decisions.'},
 {'title': 'Business Development Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Problem Solving'],
  'category': 'Sales & Business Development',
  'description': 'Identify prospects, communicate with clients and support business growth.'},
 {'title': 'Sales Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Time Management'],
  'category': 'Sales & Business Development',
  'description': 'Engage customers and support sales activities.'},
 {'title': 'Inside Sales Executive',
  'required_skills': ['Communication', 'English', 'Customer Service', 'Excel'],
  'category': 'Sales & Business Development',
  'description': 'Handle leads, calls and customer follow-ups.'},
 {'title': 'Operations Executive',
  'required_skills': ['Excel', 'Communication', 'Problem Solving', 'Time Management'],
  'category': 'Operations',
  'description': 'Coordinate daily operational activities and maintain records.'},
 {'title': 'HR Executive',
  'required_skills': ['Communication', 'English', 'Excel', 'Word'],
  'category': 'HR & Administration',
  'description': 'Support recruitment, employee records and HR operations.'},
 {'title': 'HR Recruiter',
  'required_skills': ['Communication', 'English', 'Excel', 'Problem Solving'],
  'category': 'HR & Recruitment',
  'description': 'Source candidates, coordinate interviews and maintain recruitment records.'},
 {'title': 'Talent Acquisition Executive',
  'required_skills': ['Communication', 'English', 'Excel'],
  'category': 'HR & Recruitment',
  'description': 'Support candidate sourcing and recruitment processes.'},
 {'title': 'Admin Executive',
  'required_skills': ['Excel', 'Word', 'Communication', 'Time Management'],
  'category': 'Administration',
  'description': 'Manage administrative records, documentation and coordination.'}]


# =========================================================
# SKILL ALIASES
# =========================================================

LOCAL_ALIASES = {
    **SKILL_ALIASES,

    "js": "JavaScript",
    "html5": "HTML",
    "css3": "CSS",

    "react.js": "React",
    "reactjs": "React",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "express.js": "Express",
    "expressjs": "Express",

    "fast api": "FastAPI",

    "mongo db": "MongoDB",
    "mongodb": "MongoDB",

    "postgres": "PostgreSQL",

    "amazon web services": "AWS",

    "google cloud platform": "Google Cloud",
    "gcp": "Google Cloud",

    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "powerbi": "Power BI",

    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "ms word": "Word",
    "microsoft word": "Word",
    "react js": "React",
    "fast-api": "FastAPI",
    "mongo-db": "MongoDB",
    "power-bi": "Power BI",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "customer support": "Customer Service",
    "customer service": "Customer Service",
    "basic computer": "Basic Computer Skills",
    "basic computer skills": "Basic Computer Skills",
    "email": "Email Communication",
}


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):
    """
    Convert a skill into one canonical comparison format.
    """

    if not skill:
        return ""

    normalized = str(skill).strip().lower()

    # Normalize common separators.
    normalized = normalized.replace("_", " ")
    normalized = " ".join(normalized.split())

    # Direct alias lookup.
    if normalized in LOCAL_ALIASES:
        normalized = LOCAL_ALIASES[normalized].strip().lower()

    # Remove dots so:
    # node.js == nodejs
    # react.js == reactjs
    normalized = normalized.replace(".", "")

    # Remove spaces for consistent comparison.
    normalized = normalized.replace(" ", "")

    return normalized


# =========================================================
# DISPLAY SKILL
# =========================================================

def display_skill(skill):
    """
    Return a clean canonical display name.
    """

    if not skill:
        return ""

    normalized = normalize_skill(skill)

    display_map = {
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "c": "C",
        "c++": "C++",
        "c#": "C#",

        "html": "HTML",
        "css": "CSS",
        "react": "React",
        "vuejs": "Vue.js",
        "angular": "Angular",
        "tailwindcss": "Tailwind CSS",
        "bootstrap": "Bootstrap",

        "nodejs": "Node.js",
        "express": "Express",
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "restapi": "REST API",

        "sql": "SQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "postgresql": "PostgreSQL",
        "sqlite": "SQLite",
        "firebase": "Firebase",
        "nosql": "NoSQL",

        "aws": "AWS",
        "azure": "Azure",
        "googlecloud": "Google Cloud",

        "git": "Git",
        "github": "GitHub",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "jenkins": "Jenkins",
        "ci/cd": "CI/CD",

        "artificialintelligence": "Artificial Intelligence",
        "machinelearning": "Machine Learning",
        "deeplearning": "Deep Learning",
        "tensorflow": "TensorFlow",
        "keras": "Keras",
        "pytorch": "PyTorch",
        "scikitlearn": "Scikit-learn",

        "pandas": "Pandas",
        "numpy": "NumPy",
        "matplotlib": "Matplotlib",
        "seaborn": "Seaborn",
        "powerbi": "Power BI",
        "tableau": "Tableau",
        "excel": "Excel",
        "word": "Word",
        "communication": "Communication",
        "english": "English",
        "customerservice": "Customer Service",
        "problemsolving": "Problem Solving",
        "emailcommunication": "Email Communication",
        "dataentry": "Data Entry",
        "basiccomputerskills": "Basic Computer Skills",
        "timemanagement": "Time Management",
        "teamwork": "Teamwork",
        "typing": "Typing",
        "selenium": "Selenium",
        "php": "PHP",
        "linux": "Linux",
        "springboot": "Spring Boot"
    }

    return display_map.get(normalized, str(skill).strip())


# =========================================================
# UNIQUE CANONICAL SKILLS
# =========================================================

def unique_canonical_skills(skills):
    """
    Remove duplicates and return clean display names.
    """

    result = []
    seen = set()

    if not isinstance(skills, list):
        return result

    for skill in skills:

        canonical = normalize_skill(skill)

        if not canonical:
            continue

        if canonical not in seen:
            seen.add(canonical)
            result.append(display_skill(skill))

    return result


# =========================================================
# RECOMMEND JOBS
# =========================================================

@router.post("/recommend-jobs")
async def recommend_jobs(data: dict):

    resume_skills = data.get("resume_skills", [])

    if not isinstance(resume_skills, list):
        resume_skills = []

    # -----------------------------------------------------
    # Normalize resume skills
    # -----------------------------------------------------

    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
        if normalize_skill(skill)
    }

    recommendations = []

    # -----------------------------------------------------
    # Compare every job
    # -----------------------------------------------------

    for job in JOB_ROLES:

        required_skills = unique_canonical_skills(
            job["required_skills"]
        )

        matched_skills = []
        missing_skills = []

        # -------------------------------------------------
        # Find matched and missing skills
        # -------------------------------------------------

        for skill in required_skills:

            canonical_required = normalize_skill(skill)

            if canonical_required in resume_skill_set:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

        # -------------------------------------------------
        # Calculate percentage
        # -------------------------------------------------

        if required_skills:

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

            "category": job.get("category", "Other"),

            "company": "Recommended Role",

            "location": "India",

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

        "resume_skills": unique_canonical_skills(
            resume_skills
        ),

        "total_jobs_analyzed": len(
            recommendations
        ),

        "recommendations": recommendations
    }
