# =========================================================
# SKILL EXTRACTOR
# AI JOB SKILL ANALYZER
# =========================================================


SKILLS = [

    # -----------------------------------------------------
    # Programming Languages
    # -----------------------------------------------------
    "Python", "Java", "JavaScript", "C", "C++", "C#",

    # -----------------------------------------------------
    # Frontend
    # -----------------------------------------------------
    "HTML", "CSS", "React", "Vue.js", "Angular",
    "Tailwind CSS", "Bootstrap",

    # -----------------------------------------------------
    # Backend
    # -----------------------------------------------------
    "Node.js", "Express", "FastAPI", "Flask", "Django",
    "REST API", "RESTful API",

    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------
    "SQL", "MySQL", "MongoDB", "PostgreSQL", "SQLite",
    "Firebase", "NoSQL",

    # -----------------------------------------------------
    # Cloud
    # -----------------------------------------------------
    "AWS", "Azure", "Google Cloud", "GCP",

    # -----------------------------------------------------
    # DevOps / Tools
    # -----------------------------------------------------
    "Git", "GitHub", "Docker", "Kubernetes", "Jenkins", "CI/CD",

    # -----------------------------------------------------
    # AI / Machine Learning
    # -----------------------------------------------------
    "Artificial Intelligence", "Machine Learning", "Deep Learning",
    "TensorFlow", "Keras", "PyTorch", "Scikit-learn",
    "CNN", "NLP", "Computer Vision", "OpenCV",

    # -----------------------------------------------------
    # Data Science
    # -----------------------------------------------------
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Power BI",
    "Tableau", "Excel", "Big Data", "Hadoop", "MapReduce",

    # -----------------------------------------------------
    # BPO / Customer Support / Business
    # -----------------------------------------------------
    "Communication Skills",
    "English",
    "English Communication",
    "Customer Service",
    "Customer Support",
    "Problem Solving",
    "Active Listening",
    "Word",
    "Email Communication",
    "Email Support",
    "Data Entry",
    "Basic Computer Skills",
    "Computer Skills",
    "Time Management",
    "Teamwork",
    "Customer Relationship Management",
    "CRM",
    "Typing Skills",
    "Typing",
    "Voice Process",
    "Non-Voice Process",
    "Chat Support",
    "BPO",
    "Back Office",
    "Process Associate",
    "Sales",
    "Negotiation",
    "Presentation Skills",
    "Leadership",
    "Adaptability",
    "Attention to Detail",
]


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    # Python
    "python3": "Python",

    # JavaScript
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ecmascript": "JavaScript",

    # HTML
    "html5": "HTML",

    # CSS
    "css3": "CSS",

    # React
    "react.js": "React",
    "reactjs": "React",

    # Vue
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",

    # Node
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    # Express
    "express.js": "Express",
    "expressjs": "Express",

    # FastAPI
    "fast api": "FastAPI",
    "fast-api": "FastAPI",

    # MongoDB
    "mongo db": "MongoDB",
    "mongodb": "MongoDB",

    # PostgreSQL
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    # AWS
    "amazon web services": "AWS",

    # Google Cloud
    "google cloud platform": "Google Cloud",
    "google cloud": "Google Cloud",
    "gcp": "Google Cloud",

    # Scikit-learn
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    # Power BI
    "powerbi": "Power BI",
    "power-bi": "Power BI",

    # REST API
    "restful api": "REST API",

    # CI/CD
    "continuous integration": "CI/CD",
    "continuous delivery": "CI/CD",

    # -----------------------------------------------------
    # BPO / Customer Support aliases
    # -----------------------------------------------------
    "communication": "Communication Skills",
    "communication skill": "Communication Skills",
    "communication skills": "Communication Skills",

    "english communication": "English Communication",

    "customer service": "Customer Service",
    "customer support": "Customer Support",

    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",

    "active listening": "Active Listening",

    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "ms-excel": "Excel",

    "ms word": "Word",
    "microsoft word": "Word",
    "ms-word": "Word",

    "email communication": "Email Communication",
    "email support": "Email Support",

    "data entry": "Data Entry",

    "basic computer skills": "Basic Computer Skills",
    "computer skills": "Computer Skills",

    "time management": "Time Management",
    "teamwork": "Teamwork",

    "customer relationship management": "Customer Relationship Management",
    "crm": "Customer Relationship Management",

    "typing skills": "Typing Skills",
    "typing": "Typing",

    "voice process": "Voice Process",
    "non voice process": "Non-Voice Process",
    "non-voice process": "Non-Voice Process",

    "chat support": "Chat Support",
    "back office": "Back Office",
    "process associate": "Process Associate",

    "presentation skills": "Presentation Skills",
    "attention to detail": "Attention to Detail",
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Convert text into a consistent searchable format.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Normalize common separators/punctuation.
    for character in ["_", "-", ".", "/", ",", ":", ";", "(", ")"]:
        text = text.replace(character, " ")

    # Remove extra spaces.
    text = " ".join(text.split())

    return text


# =========================================================
# CANONICAL SKILL MAP
# =========================================================

def build_canonical_map():
    """
    Create normalized skill -> canonical skill mapping.
    """

    mapping = {}

    for skill in SKILLS:
        mapping[normalize_text(skill)] = skill

    for alias, canonical in SKILL_ALIASES.items():
        mapping[normalize_text(alias)] = canonical

    return mapping


CANONICAL_MAP = build_canonical_map()


# =========================================================
# CHECK SKILL
# =========================================================

def skill_found(text, skill):
    """
    Check whether a skill exists in the text.
    """

    normalized_text = normalize_text(text)
    normalized_skill = normalize_text(skill)

    if not normalized_text or not normalized_skill:
        return False

    text_words = set(normalized_text.split())
    skill_words = normalized_skill.split()

    if len(skill_words) == 1:
        return normalized_skill in text_words

    return normalized_skill in normalized_text


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):
    """
    Extract technical, BPO, customer-support and business skills.
    Return unique canonical skill names only.
    """

    if not text:
        return []

    normalized_text = normalize_text(text)

    found_skills = []
    seen = set()

    # Main skill list.
    for skill in SKILLS:
        if skill_found(normalized_text, skill):
            canonical = CANONICAL_MAP.get(
                normalize_text(skill),
                skill
            )

            key = normalize_text(canonical)

            if key not in seen:
                found_skills.append(canonical)
                seen.add(key)

    # Aliases.
    for alias, canonical in SKILL_ALIASES.items():
        if skill_found(normalized_text, alias):
            canonical = CANONICAL_MAP.get(
                normalize_text(canonical),
                canonical
            )

            key = normalize_text(canonical)

            if key not in seen:
                found_skills.append(canonical)
                seen.add(key)

    return found_skills
