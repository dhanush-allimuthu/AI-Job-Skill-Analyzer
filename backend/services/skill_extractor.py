# =========================================================
# SKILL EXTRACTOR
# =========================================================


SKILLS = [

    # -----------------------------------------------------
    # Programming Languages
    # -----------------------------------------------------

    "Python",
    "Java",
    "JavaScript",
    "C",
    "C++",
    "C#",


    # -----------------------------------------------------
    # Frontend
    # -----------------------------------------------------

    "HTML",
    "CSS",
    "React",
    "Vue.js",
    "Angular",
    "Tailwind CSS",
    "Bootstrap",


    # -----------------------------------------------------
    # Backend
    # -----------------------------------------------------

    "Node.js",
    "Express",
    "FastAPI",
    "Flask",
    "Django",
    "REST API",
    "RESTful API",


    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------

    "SQL",
    "MySQL",
    "MongoDB",
    "PostgreSQL",
    "SQLite",
    "Firebase",
    "NoSQL",


    # -----------------------------------------------------
    # Cloud
    # -----------------------------------------------------

    "AWS",
    "Azure",
    "Google Cloud",
    "GCP",


    # -----------------------------------------------------
    # DevOps / Tools
    # -----------------------------------------------------

    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "CI/CD",


    # -----------------------------------------------------
    # AI / Machine Learning
    # -----------------------------------------------------

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
    "OpenCV",


    # -----------------------------------------------------
    # Data Science
    # -----------------------------------------------------

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


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    "python3": "Python",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "html5": "HTML",

    "css3": "CSS",

    "react.js": "React",
    "reactjs": "React",

    "vue": "Vue.js",
    "vuejs": "Vue.js",

    "node": "Node.js",
    "nodejs": "Node.js",

    "express.js": "Express",
    "expressjs": "Express",

    "fast api": "FastAPI",

    "mongo db": "MongoDB",
    "mongodb": "MongoDB",

    "postgres": "PostgreSQL",

    "amazon web services": "AWS",

    "google cloud platform": "Google Cloud",

    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "powerbi": "Power BI"
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Convert text into a consistent format.
    """

    if not text:
        return ""

    text = text.lower()

    # Replace common separators
    text = text.replace("-", " ")
    text = text.replace("_", " ")

    # Remove extra spaces
    text = " ".join(text.split())

    return text


# =========================================================
# CHECK SKILL
# =========================================================

def skill_found(text, skill):
    """
    Check whether a skill exists in the text.
    """

    normalized_text = normalize_text(text)

    normalized_skill = normalize_text(skill)

    # Exact phrase / word matching
    words = normalized_text.split()

    skill_words = normalized_skill.split()

    # Single word skill
    if len(skill_words) == 1:

        return normalized_skill in words


    # Multi-word skill
    text_string = " ".join(words)

    return normalized_skill in text_string


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):
    """
    Extract technical skills from resume or job description.
    """

    if not text:
        return []


    found_skills = []


    # -----------------------------------------------------
    # Check main skill list
    # -----------------------------------------------------

    for skill in SKILLS:

        if skill_found(text, skill):

            if skill not in found_skills:

                found_skills.append(skill)


    # -----------------------------------------------------
    # Check aliases
    # -----------------------------------------------------

    normalized_text = normalize_text(text)


    for alias, main_skill in SKILL_ALIASES.items():

        normalized_alias = normalize_text(alias)

        if normalized_alias in normalized_text:

            if main_skill not in found_skills:

                found_skills.append(main_skill)


    return found_skills


