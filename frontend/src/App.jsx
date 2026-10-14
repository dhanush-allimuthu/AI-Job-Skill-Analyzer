import { useEffect, useMemo, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const navItems = [
  { id: "dashboard", label: "Home", icon: "⌂" },
  { id: "resume", label: "Resume Analysis", icon: "▣" },
  { id: "skills", label: "Skill Gap", icon: "◈" },
  { id: "jobs", label: "Job Matches", icon: "▰" },
  { id: "roadmap", label: "Learning Roadmap", icon: "◇" },
];

const SAMPLE_JD = `We are hiring a Python Developer to join our backend engineering team.

Responsibilities:
- Build and maintain REST APIs using Python and FastAPI
- Design and optimize SQL database schemas
- Write clean, testable, well-documented code
- Collaborate with frontend engineers integrating React applications
- Deploy and monitor services on AWS
- Work with Docker to containerize services

Requirements:
- Strong experience with Python
- Experience with FastAPI or a similar framework
- Solid understanding of SQL databases
- Familiarity with React for full-stack collaboration
- Experience with Docker
- Exposure to AWS cloud services
- Understanding of REST API design principles`;

const fallbackJobs = [
  {
    title: "Frontend Developer",
    company: "Tech Solutions",
    location: "Chennai",
    match_percentage: 92,
    required_skills: ["React", "JavaScript", "CSS"],
  },
  {
    title: "Data Analyst",
    company: "Analytics Labs",
    location: "Bangalore",
    match_percentage: 88,
    required_skills: ["Python", "SQL", "Excel"],
  },
  {
    title: "Full Stack Developer",
    company: "Digital Systems",
    location: "Chennai",
    match_percentage: 85,
    required_skills: ["React", "Node.js", "MongoDB"],
  },
  {
    title: "Python Developer",
    company: "Cloud Matrix",
    location: "Coimbatore",
    match_percentage: 82,
    required_skills: ["Python", "Flask", "SQL"],
  },
  {
    title: "Backend Developer",
    company: "CodeCraft",
    location: "Hyderabad",
    match_percentage: 79,
    required_skills: ["Node.js", "Express", "MongoDB"],
  },
  {
    title: "Junior ML Engineer",
    company: "AI Labs",
    location: "Bangalore",
    match_percentage: 74,
    required_skills: ["Python", "Machine Learning", "TensorFlow"],
  },
];

const fallbackUserSkills = [
  { name: "Python", level: 90, type: "strong" },
  { name: "JavaScript", level: 82, type: "strong" },
  { name: "HTML / CSS", level: 88, type: "strong" },
  { name: "React", level: 70, type: "medium" },
  { name: "SQL", level: 72, type: "medium" },
  { name: "Git & GitHub", level: 80, type: "strong" },
];

const fallbackMissingSkills = [
  { name: "Advanced React", priority: "High", progress: 35 },
  { name: "Node.js", priority: "High", progress: 45 },
  { name: "Docker", priority: "Medium", progress: 20 },
  { name: "AWS", priority: "Medium", progress: 15 },
  { name: "System Design", priority: "Low", progress: 10 },
];

const fallbackRoadmap = [
  {
    number: "01",
    title: "Master Web Fundamentals",
    duration: "2 Weeks",
    description: "Strengthen HTML, CSS, JavaScript and responsive web development.",
    topics: ["HTML5", "CSS Flexbox & Grid", "JavaScript ES6+", "Responsive Design"],
  },
  {
    number: "02",
    title: "Become Strong in React",
    duration: "3 Weeks",
    description: "Build production-style React applications and understand component architecture.",
    topics: ["Components", "Hooks", "Routing", "API Integration"],
  },
  {
    number: "03",
    title: "Learn Backend Development",
    duration: "3 Weeks",
    description: "Build REST APIs and connect frontend applications with databases.",
    topics: ["Node.js", "Express", "REST API", "MongoDB"],
  },
  {
    number: "04",
    title: "Build Real Projects",
    duration: "4 Weeks",
    description: "Create portfolio-ready projects that demonstrate practical development skills.",
    topics: ["E-Commerce", "Job Portal", "AI Integration", "Deployment"],
  },
  {
    number: "05",
    title: "Interview Preparation",
    duration: "2 Weeks",
    description: "Prepare technical, aptitude and HR interview skills.",
    topics: ["DSA Basics", "SQL Questions", "Aptitude", "HR Questions"],
  },
];

function normalizeRoadmap(raw) {
  if (!raw) return [];

  const source = raw.roadmap || raw.learning_roadmap || raw.data || raw;

  if (Array.isArray(source)) {
    return source.map((item, index) => ({
      number: String(index + 1).padStart(2, "0"),
      title: item.title || item.skill || `Learning Step ${index + 1}`,
      duration: item.duration || "Self-paced",
      description: item.description || item.project || "Build practical knowledge for this skill.",
      topics: Array.isArray(item.topics) ? item.topics : [],
      resource: item.resource || "",
      project: item.project || "",
    }));
  }

  if (typeof source === "object") {
    return Object.entries(source).map(([skill, info], index) => {
      const value = Array.isArray(info) ? { topics: info } : info || {};
      return {
        number: String(index + 1).padStart(2, "0"),
        title: value.title || skill,
        duration: value.duration || "Self-paced",
        description: value.description || value.project || `Learn ${skill} through guided practice.`,
        topics: Array.isArray(value.topics) ? value.topics : [],
        resource: value.resource || "",
        project: value.project || "",
      };
    });
  }

  return [];
}

function getJobCategory(title = "") {
  const value = title.toLowerCase();

  if (
    value.includes("bpo") ||
    value.includes("customer support") ||
    value.includes("customer service") ||
    value.includes("voice process") ||
    value.includes("non-voice") ||
    value.includes("chat support") ||
    value.includes("process associate") ||
    value.includes("back office") ||
    value.includes("data entry")
  ) return "BPO & Customer Support";

  if (
    value.includes("hr ") ||
    value.startsWith("hr") ||
    value.includes("recruiter") ||
    value.includes("talent acquisition") ||
    value.includes("admin")
  ) return "HR & Administration";

  if (
    value.includes("sales") ||
    value.includes("business development") ||
    value.includes("relationship executive") ||
    value.includes("business analyst")
  ) return "Sales & Business";

  if (
    value.includes("data analyst") ||
    value.includes("data scientist") ||
    value.includes("data engineer") ||
    value.includes("business intelligence") ||
    value.includes("bi analyst")
  ) return "Data & Analytics";

  if (
    value.includes("machine learning") ||
    value.includes("ml engineer") ||
    value.includes("ai engineer") ||
    value.includes("deep learning") ||
    value.includes("nlp") ||
    value.includes("computer vision")
  ) return "AI & ML";

  if (
    value.includes("cloud") ||
    value.includes("devops") ||
    value.includes("aws") ||
    value.includes("azure") ||
    value.includes("system administrator")
  ) return "Cloud & DevOps";

  if (
    value.includes("qa") ||
    value.includes("tester") ||
    value.includes("testing") ||
    value.includes("automation")
  ) return "Testing & QA";

  if (
    value.includes("support engineer") ||
    value.includes("technical support") ||
    value.includes("application support") ||
    value.includes("it support")
  ) return "IT Support";

  return "IT & Software";
}

function normalizeJobs(data) {
  const list = data?.recommendations || data?.jobs || data?.data || [];
  return Array.isArray(list)
    ? list.map((job) => {
        const title = job.title || job.role || "Untitled Role";
        return {
          ...job,
          title,
          company: job.company || "Recommended Role",
          location: job.location || "India",
          category: job.category || getJobCategory(title),
          experience: job.experience || "Fresher / Entry Level",
          work_mode: job.work_mode || job.workMode || "Full-time",
          match_percentage: Number(
            job.match_percentage ?? job.match ?? job.score ?? 0
          ),
          required_skills: Array.isArray(job.required_skills)
            ? job.required_skills
            : Array.isArray(job.skills)
              ? job.skills
              : [],
          matched_skills: Array.isArray(job.matched_skills)
            ? job.matched_skills
            : [],
          missing_skills: Array.isArray(job.missing_skills)
            ? job.missing_skills
            : [],
        };
      })
    : [];
}


const ADVANCED_ROADMAPS = {
  "Frontend Developer": [
    {
      number: "01",
      title: "Advanced React",
      duration: "7 Days",
      description: "Move from basic React usage to production-level component architecture and performance.",
      topics: ["Advanced component patterns", "Custom hooks", "Context and state optimization", "Reusable component architecture", "Build an advanced React feature"],
      resource: "https://react.dev/learn",
      project: "Build an Advanced React Job Dashboard"
    },
    {
      number: "02",
      title: "TypeScript for React",
      duration: "6 Days",
      description: "Add type safety and scalable development practices to React applications.",
      topics: ["Types and interfaces", "Generics", "Typed React props", "Typed API responses", "Convert a React module to TypeScript"],
      resource: "https://www.typescriptlang.org/docs/",
      project: "Convert a React Project to TypeScript"
    },
    {
      number: "03",
      title: "Frontend Testing",
      duration: "5 Days",
      description: "Learn practical testing for components, interactions and user flows.",
      topics: ["Testing fundamentals", "React Testing Library", "Component testing", "User interaction testing", "Write automated frontend tests"],
      resource: "https://testing-library.com/docs/react-testing-library/intro/",
      project: "Add Automated Tests to a React Application"
    },
    {
      number: "04",
      title: "Performance Optimization",
      duration: "5 Days",
      description: "Improve application speed, bundle size and real-world web performance.",
      topics: ["Web performance fundamentals", "Code splitting", "Lazy loading", "Memoization", "Core Web Vitals"],
      resource: "https://web.dev/learn/performance/",
      project: "Optimize a Production React Application"
    },
    {
      number: "05",
      title: "Production Deployment",
      duration: "4 Days",
      description: "Prepare a frontend application for production deployment and monitoring.",
      topics: ["Production builds", "Environment variables", "Deployment configuration", "CI/CD basics", "Production monitoring"],
      resource: "https://vercel.com/docs",
      project: "Deploy a Production React Application"
    }
  ],
  "Full Stack Developer": [
    {
      number: "01",
      title: "Advanced Full Stack Architecture",
      duration: "7 Days",
      description: "Design scalable frontend, backend, database and API layers.",
      topics: ["Frontend-backend architecture", "REST API integration", "Authentication", "Error handling", "Production architecture"],
      resource: "https://developer.mozilla.org/en-US/docs/Learn",
      project: "Build a Production Full Stack Application"
    },
    {
      number: "02",
      title: "TypeScript",
      duration: "6 Days",
      description: "Use TypeScript to improve maintainability across full stack applications.",
      topics: ["Types and interfaces", "Generics", "Type-safe React props", "Typed APIs", "Type-safe full stack development"],
      resource: "https://www.typescriptlang.org/docs/",
      project: "Build a Type-Safe Full Stack App"
    },
    {
      number: "03",
      title: "Authentication & Security",
      duration: "6 Days",
      description: "Implement secure authentication and protected application flows.",
      topics: ["Authentication fundamentals", "JWT", "Password security", "Role-based access", "Protected frontend and backend routes"],
      resource: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication",
      project: "Build an Authenticated Full Stack App"
    },
    {
      number: "04",
      title: "Database & API Optimization",
      duration: "5 Days",
      description: "Improve API response time and database performance.",
      topics: ["Database indexing", "Query optimization", "Pagination", "Caching basics", "API performance"],
      resource: "https://www.mongodb.com/docs/",
      project: "Optimize a Full Stack E-Commerce API"
    }
  ],
  "Python Developer": [
    {
      number: "01",
      title: "Advanced Python",
      duration: "7 Days",
      description: "Strengthen Python with advanced language features and production practices.",
      topics: ["Decorators", "Generators", "Async programming", "Exception handling", "Logging and clean architecture"],
      resource: "https://docs.python.org/3/tutorial/",
      project: "Build a Production Python Service"
    },
    {
      number: "02",
      title: "FastAPI & REST API Architecture",
      duration: "6 Days",
      description: "Build scalable REST APIs with validation, documentation and security.",
      topics: ["FastAPI fundamentals", "Pydantic validation", "Dependency injection", "Authentication", "API documentation"],
      resource: "https://fastapi.tiangolo.com/tutorial/",
      project: "Build a Production Resume API"
    },
    {
      number: "03",
      title: "Testing & Deployment",
      duration: "5 Days",
      description: "Test and deploy Python applications using production practices.",
      topics: ["Unit testing", "API testing", "Mocking", "Docker deployment", "Production monitoring"],
      resource: "https://docs.pytest.org/",
      project: "Test and Deploy a Python Application"
    }
  ],
  "Backend Developer": [
    {
      number: "01",
      title: "Advanced Backend Architecture",
      duration: "7 Days",
      description: "Design maintainable and scalable backend services.",
      topics: ["Layered architecture", "REST API design", "Authentication", "Error handling", "Caching"],
      resource: "https://fastapi.tiangolo.com/tutorial/",
      project: "Build a Production Backend API"
    },
    {
      number: "02",
      title: "Database Optimization",
      duration: "5 Days",
      description: "Improve database design and query performance.",
      topics: ["Database indexing", "Query optimization", "Transactions", "Relationships", "Performance tuning"],
      resource: "https://www.postgresql.org/docs/",
      project: "Optimize a Backend Database"
    },
    {
      number: "03",
      title: "API Testing",
      duration: "4 Days",
      description: "Create reliable automated tests for backend services.",
      topics: ["API testing fundamentals", "Unit tests", "Integration tests", "Mocking", "Automated API test suites"],
      resource: "https://fastapi.tiangolo.com/tutorial/testing/",
      project: "Create an Automated API Test Suite"
    }
  ],
  "Data Analyst": [
    {
      number: "01",
      title: "Advanced SQL",
      duration: "6 Days",
      description: "Use advanced SQL techniques for business and analytical problems.",
      topics: ["Window functions", "CTEs", "Subqueries", "Query optimization", "Analytical SQL"],
      resource: "https://www.w3schools.com/sql/",
      project: "Build an Advanced Sales Analytics Database"
    },
    {
      number: "02",
      title: "Power BI Dashboarding",
      duration: "5 Days",
      description: "Create interactive business intelligence dashboards.",
      topics: ["Data modeling", "Power BI visuals", "DAX basics", "Interactive dashboards", "Dashboard publishing"],
      resource: "https://learn.microsoft.com/power-bi/",
      project: "Build a Business Intelligence Dashboard"
    },
    {
      number: "03",
      title: "Data Storytelling",
      duration: "4 Days",
      description: "Turn analytical results into clear business insights.",
      topics: ["Business KPIs", "Chart selection", "Dashboard design", "Insight generation", "Present analytical findings"],
      resource: "https://learn.microsoft.com/power-bi/",
      project: "Create an Executive Sales Report"
    }
  ],
  "Machine Learning Engineer": [
    {
      number: "01",
      title: "Advanced Machine Learning",
      duration: "8 Days",
      description: "Improve model quality with advanced machine learning workflows.",
      topics: ["Feature engineering", "Model evaluation", "Cross validation", "Hyperparameter tuning", "ML pipelines"],
      resource: "https://scikit-learn.org/stable/user_guide.html",
      project: "Build an End-to-End ML Pipeline"
    },
    {
      number: "02",
      title: "Model Deployment",
      duration: "6 Days",
      description: "Deploy machine learning models as production-ready services.",
      topics: ["Model serialization", "REST API deployment", "FastAPI for ML", "Docker for ML", "Prediction monitoring"],
      resource: "https://fastapi.tiangolo.com/",
      project: "Deploy a Machine Learning API"
    }
  ],
  "Cloud Developer": [
    {
      number: "01",
      title: "AWS Architecture",
      duration: "7 Days",
      description: "Understand how to design secure and scalable cloud applications.",
      topics: ["AWS architecture", "EC2", "S3", "IAM", "Cloud networking basics"],
      resource: "https://aws.amazon.com/getting-started/",
      project: "Design and Deploy a Cloud Application"
    },
    {
      number: "02",
      title: "Cloud Deployment",
      duration: "5 Days",
      description: "Deploy and monitor containerized applications in the cloud.",
      topics: ["Application deployment", "Environment configuration", "Docker deployment", "Cloud logging", "Cloud monitoring"],
      resource: "https://docs.aws.amazon.com/",
      project: "Deploy a Dockerized Application on AWS"
    }
  ]
};

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem("ajsa-theme") || "dark";
    } catch {
      return "dark";
    }
  });

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [resumeSkills, setResumeSkills] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);

  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [error, setError] = useState("");
  const [toast, setToast] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [search, setSearch] = useState("");
  const [jobSort, setJobSort] = useState("high-low");
  const [jobFilter, setJobFilter] = useState("all");
  const [jobCategory, setJobCategory] = useState("all");
  const [openRoadmap, setOpenRoadmap] = useState(0);
  const [completedTopics, setCompletedTopics] = useState({});
  const [jobModal, setJobModal] = useState(null);

  const fileInputRef = useRef(null);
  const toastTimer = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("ajsa-theme", theme);
    } catch {
      // Ignore storage errors.
    }
  }, [theme]);

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("ajsa-progress") || "{}");
      setCompletedTopics(saved);
    } catch {
      setCompletedTopics({});
    }
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem("ajsa-progress", JSON.stringify(completedTopics));
    } catch {
      // Ignore storage errors.
    }
  }, [completedTopics]);

  useEffect(() => {
    return () => window.clearTimeout(toastTimer.current);
  }, []);

  const showToast = (message) => {
    setToast(message);
    window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(null), 4500);
  };

  const navigate = (page) => {
    setActivePage(page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const resetAnalysis = () => {
    setAnalyzed(false);
    setResumeText("");
    setResumeSkills([]);
    setAnalysis(null);
    setSkillGap(null);
    setRecommendations([]);
    setRoadmap([]);
    setSelectedJob(null);
    setCompletedTopics({});
    try {
      localStorage.removeItem("ajsa-progress");
    } catch {
      // Ignore storage errors.
    }
  };

  const validateAndSetFile = (file) => {
    if (!file) return;

    if (
      file.type !== "application/pdf" &&
      !file.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please upload a PDF resume.");
      showToast("Please upload a PDF resume.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("Resume file must be under 5MB.");
      showToast("Resume file must be under 5MB.");
      return;
    }

    setError("");
    setResumeFile(file);
    resetAnalysis();
  };

  const handleFileChange = (event) => {
    validateAndSetFile(event.target.files?.[0]);
    event.target.value = "";
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);
    validateAndSetFile(event.dataTransfer.files?.[0]);
  };

  const apiRequest = async (path, options = {}) => {
    const response = await fetch(`${API_URL}${path}`, options);
    let data = {};

    try {
      data = await response.json();
    } catch {
      data = {};
    }

    if (!response.ok) {
      throw new Error(data.detail || data.message || `Request failed (${response.status})`);
    }

    return data;
  };

  const analyzeResume = async () => {
    if (!resumeFile) {
      setError("Please upload your resume first.");
      showToast("Please upload your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter the target job description.");
      showToast("Please enter the target job description.");
      return;
    }

    setLoading(true);
    setError("");
    setLoadingStep(0);
    setRoadmap([]);
    setSelectedJob(null);
    setCompletedTopics({});
    setOpenRoadmap(0);

    try {
      const form = new FormData();
      form.append("file", resumeFile);

      const uploadData = await apiRequest("/api/upload-resume", {
        method: "POST",
        body: form,
      });

      setLoadingStep(1);
      const extractedText =
        uploadData.extracted_text ||
        uploadData.text ||
        "";

      setResumeText(extractedText);

      let skills = uploadData.skills || uploadData.extracted_skills || [];

      if (!skills.length && extractedText) {
        const skillData = await apiRequest("/api/extract-skills", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ resume_text: extractedText }),
        });
        skills = skillData.skills || skillData.extracted_skills || [];
      }

      setResumeSkills(skills);

      setLoadingStep(2);
      const analysisForm = new FormData();
      analysisForm.append("file", resumeFile);
      analysisForm.append("job_description", jobDescription);

      const analysisData = await apiRequest("/api/analyze-resume", {
        method: "POST",
        body: analysisForm,
      });
      setAnalysis(analysisData.analysis || analysisData);

      const gapData = await apiRequest("/api/skill-gap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_skills: skills,
          job_description: jobDescription,
        }),
      });
      setSkillGap(gapData);

      setLoadingStep(3);
      const jobsData = await apiRequest("/api/recommend-jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_skills: skills }),
      });

      const normalized = normalizeJobs(jobsData);
      setRecommendations(normalized);

      setAnalyzed(true);
      navigate("skills");
      showToast("Resume analysis completed successfully.");
    } catch (err) {
      console.error(err);

      const message =
        err instanceof TypeError
          ? "Failed to fetch. Make sure FastAPI is running on http://127.0.0.1:8000 and CORS is enabled."
          : err.message ||
            "Unable to connect to the backend. Please make sure FastAPI is running.";

      setError(message);
      showToast(message);
    } finally {
      setLoading(false);
      setLoadingStep(0);
    }
  };

  const loadRoadmap = async (missingSkills, job = null) => {
    const skills = Array.isArray(missingSkills) ? missingSkills : [];
    const jobTitle = job?.title || job?.role || "";
    const jobMatch = Number(job?.match_percentage ?? job?.match ?? 0);

    // 100% match: show advanced learning instead of a missing-skill roadmap.
    if (skills.length === 0 && jobMatch >= 100) {
      const advanced = ADVANCED_ROADMAPS[jobTitle];

      if (advanced?.length) {
        setRoadmap(advanced);
      } else {
        setRoadmap([
          {
            number: "01",
            title: "Advanced Career Development",
            duration: "7 Days",
            description:
              "You already match the core skills for this role. Focus on advanced concepts, production practices and portfolio quality.",
            topics: [
              "Advanced role-specific concepts",
              "Production-ready architecture",
              "Testing and debugging",
              "Performance optimization",
              "Deployment and monitoring"
            ],
            resource: "https://developer.mozilla.org/",
            project: `Build an advanced ${jobTitle || "developer"} project`
          }
        ]);
      }

      setOpenRoadmap(0);
      return;
    }

    // Less than 100%: use the FastAPI missing-skill roadmap.
    if (skills.length > 0) {
      try {
        const data = await apiRequest("/api/learning-roadmap", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ missing_skills: skills }),
        });

        const normalized = normalizeRoadmap(data);
        setRoadmap(normalized.length ? normalized : fallbackRoadmap);
        setOpenRoadmap(0);
      } catch (err) {
        console.warn("Roadmap API failed:", err);
        setRoadmap(fallbackRoadmap);
        setOpenRoadmap(0);
        showToast("Roadmap API unavailable. Showing the default roadmap.");
      }

      return;
    }

    setRoadmap(fallbackRoadmap);
    setOpenRoadmap(0);
  };

  const selectJob = async (job) => {
    setSelectedJob(job);
    setCompletedTopics({});
    setOpenRoadmap(0);

    try {
      localStorage.removeItem("ajsa-progress");
    } catch {
      // Ignore storage errors.
    }

    await loadRoadmap(job?.missing_skills, job);
    navigate("roadmap");
  };

  const useSampleJD = () => {
    setJobDescription(SAMPLE_JD);
    setError("");
  };

  const toggleTopic = (roadmapIndex, topicIndex) => {
    const key = `${roadmapIndex}-${topicIndex}`;
    setCompletedTopics((previous) => ({
      ...previous,
      [key]: !previous[key],
    }));
  };

  const matchPercent = Math.min(
    100,
    Math.max(
      0,
      Number(
        analysis?.match_percentage ??
          analysis?.match_percent ??
          analysis?.match_score ??
          skillGap?.match_percentage ??
          skillGap?.match_percent ??
          skillGap?.match_score ??
          0
      )
    )
  );

  const matchedSkills =
    analysis?.matched_skills ||
    skillGap?.matched_skills ||
    [];

  const missingSkills =
    analysis?.missing_skills ||
    skillGap?.missing_skills ||
    [];

  const normalizedMissing = missingSkills.map((item) =>
    typeof item === "string"
      ? { name: item, priority: "Medium", progress: 0 }
      : item
  );

  const totalTopics = roadmap.reduce(
    (sum, item) => sum + (item.topics?.length || 0),
    0
  );

  const completedCount = roadmap.reduce(
    (sum, item, roadmapIndex) =>
      sum +
      (item.topics || []).filter(
        (_, topicIndex) => completedTopics[`${roadmapIndex}-${topicIndex}`]
      ).length,
    0
  );

  const roadmapProgress =
    totalTopics > 0
      ? Math.round((completedCount / totalTopics) * 100)
      : 0;

  const displayedJobs = useMemo(() => {
    const source = recommendations.length
      ? recommendations.map((job) => ({
          ...job,
          category: job.category || getJobCategory(job.title),
          experience: job.experience || "Fresher / Entry Level",
          work_mode: job.work_mode || "Full-time",
        }))
      : fallbackJobs.map((job) => ({
          ...job,
          category: getJobCategory(job.title),
          experience: "Fresher / Entry Level",
          work_mode: "Full-time",
        }));

    return source
      .filter((job) => {
        const text =
          `${job.title} ${job.company} ${job.location} ${job.category}`.toLowerCase();
        const matchesSearch = text.includes(search.toLowerCase());
        const matchesCategory =
          jobCategory === "all" || job.category === jobCategory;

        if (!matchesSearch || !matchesCategory) return false;

        if (jobFilter === "80") return job.match_percentage >= 80;
        if (jobFilter === "60") return job.match_percentage >= 60;
        return true;
      })
      .sort((a, b) =>
        jobSort === "low-high"
          ? a.match_percentage - b.match_percentage
          : b.match_percentage - a.match_percentage
      );
  }, [recommendations, search, jobFilter, jobSort, jobCategory]);

  return (
    <div className={`app ${theme}`}>
      <Header
        activePage={activePage}
        navigate={navigate}
        theme={theme}
        setTheme={setTheme}
      />

      <main className="main-content">
        {activePage === "dashboard" && <Dashboard navigate={navigate} />}

        {activePage === "resume" && (
          <ResumeAnalysis
            resumeFile={resumeFile}
            handleFileChange={handleFileChange}
            handleDrop={handleDrop}
            dragActive={dragActive}
            setDragActive={setDragActive}
            fileInputRef={fileInputRef}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            useSampleJD={useSampleJD}
            analyzeResume={analyzeResume}
            loading={loading}
            loadingStep={loadingStep}
            error={error}
          />
        )}

        {activePage === "skills" && (
          <SkillGap
            analyzed={analyzed}
            navigate={navigate}
            matchPercent={matchPercent}
            resumeSkills={resumeSkills}
            matchedSkills={matchedSkills}
            missingSkills={normalizedMissing}
          />
        )}

        {activePage === "jobs" && (
          <JobMatches
            jobs={displayedJobs}
            search={search}
            setSearch={setSearch}
            jobSort={jobSort}
            setJobSort={setJobSort}
            jobFilter={jobFilter}
            setJobFilter={setJobFilter}
            jobCategory={jobCategory}
            setJobCategory={setJobCategory}
            selectJob={selectJob}
            analyzed={analyzed}
          />
        )}

        {activePage === "roadmap" && (
          <LearningRoadmap
            roadmap={roadmap.length ? roadmap : fallbackRoadmap}
            selectedJob={selectedJob}
            openRoadmap={openRoadmap}
            setOpenRoadmap={setOpenRoadmap}
            completedTopics={completedTopics}
            toggleTopic={toggleTopic}
            roadmapProgress={roadmap.length ? roadmapProgress : 0}
          />
        )}
      </main>

      <Footer />

      {jobModal && (
        <JobModal job={jobModal} onClose={() => setJobModal(null)} />
      )}

      {toast && <div className="toast">{toast}</div>}
    </div>
  );
}

function Header({ activePage, navigate, theme, setTheme }) {
  return (
    <header className="navbar">
      <div
        className="brand"
        onClick={() => navigate("dashboard")}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") navigate("dashboard");
        }}
      >
        <div className="brand-logo">✦</div>
        <div>
          <div className="brand-name">
            CareerForge <span>AI</span>
          </div>
          <div className="brand-tagline">Analyze • Match • Grow</div>
        </div>
      </div>

      <nav className="desktop-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-link ${activePage === item.id ? "active" : ""}`}
            onClick={() => navigate(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="nav-actions">
        <button
          className="icon-button"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          title="Toggle theme"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? "☀" : "☾"}
        </button>

        <button className="icon-button profile-icon" title="Profile" aria-label="Profile">
          ♙
        </button>

        <button className="header-cta" onClick={() => navigate("resume")}>
          Get Started <span>→</span>
        </button>
      </div>
    </header>
  );
}

function Dashboard({ navigate }) {
  return (
    <div className="page">
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">✦ AI POWERED CAREER ANALYSIS</div>

          <h1>
            Build Your Career
            <br />
            With <span>AI Insights</span>
          </h1>

          <p>
            Analyze your resume, discover skill gaps, get matching job
            opportunities and a personalized learning roadmap — all in one place.
          </p>

          <div className="hero-actions">
            <button className="primary-button" onClick={() => navigate("resume")}>
              Analyze My Resume <span>→</span>
            </button>

            <button className="secondary-button" onClick={() => navigate("jobs")}>
              <span className="play-icon">▶</span>
              Explore Job Matches
            </button>
          </div>

          <div className="hero-stats">
            <div>
              <strong>AI</strong>
              <span>Resume Analysis</span>
            </div>
            <div>
              <strong>60+</strong>
              <span>Career Roles</span>
            </div>
            <div>
              <strong>24/7</strong>
              <span>Learning Guidance</span>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="glow-orb" />

          <div className="resume-floating-card">
            <div className="mini-resume-avatar">👨🏻‍💻</div>
            <div>
              <strong>RESUME</strong>
              <div className="fake-line" />
              <div className="fake-line short" />
              <div className="fake-line" />
            </div>
          </div>

          <div className="career-person">
            <div className="person-head">🙂</div>
            <div className="person-body">
              <div className="person-shirt" />
              <div className="person-laptop">▰</div>
            </div>
          </div>

          <div className="skill-floating-card">
            <div className="floating-title">
              <span>✦</span> Skill Match
            </div>
            <div className="skill-score">
              <div className="score-ring">
                <strong>AI</strong>
              </div>
              <div className="skill-list-mini">
                <span>✓ Python</span>
                <span>✓ React</span>
                <span>✓ SQL</span>
                <span className="missing">× Skill Gap</span>
              </div>
            </div>
          </div>

          <div className="job-floating-card">
            <div className="floating-title">◈ Job Matches</div>
            <MiniJob icon="〈/〉" title="Frontend Developer" score="92%" />
            <MiniJob icon="▥" title="Data Analyst" score="88%" />
            <MiniJob icon="▤" title="Full Stack Developer" score="85%" />
          </div>

          <div className="roadmap-floating-card">
            <div className="floating-title">◇ Learning Roadmap</div>
            <RoadmapMini number="1" title="Web Fundamentals" done />
            <RoadmapMini number="2" title="Advanced React" done />
            <RoadmapMini number="3" title="System Design" />
            <RoadmapMini number="4" title="Career Preparation" />
          </div>
        </div>
      </section>

      <section className="feature-grid">
        <FeatureCard icon="◉" color="purple" title="Smart Analysis" text="AI-powered resume analysis with detailed insights." />
        <FeatureCard icon="◎" color="red" title="Skill Gap Detection" text="Identify missing skills and get personalized suggestions." />
        <FeatureCard icon="▰" color="orange" title="Job Recommendations" text="Find matching job opportunities based on your profile." />
        <FeatureCard icon="▱" color="blue" title="Learning Path" text="Get a customized roadmap to upgrade your skills." />
      </section>
    </div>
  );
}

function MiniJob({ icon, title, score }) {
  return (
    <div className="mini-job">
      <span className="mini-job-icon">{icon}</span>
      <span className="mini-job-title">{title}</span>
      <strong>{score}</strong>
    </div>
  );
}

function RoadmapMini({ number, title, done }) {
  return (
    <div className="mini-roadmap">
      <div className={`roadmap-number ${done ? "done" : ""}`}>
        {done ? "✓" : number}
      </div>
      <span>{title}</span>
    </div>
  );
}

function FeatureCard({ icon, color, title, text }) {
  return (
    <div className="feature-card">
      <div className={`feature-icon ${color}`}>{icon}</div>
      <div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>
    </div>
  );
}

function ResumeAnalysis({
  resumeFile,
  handleFileChange,
  handleDrop,
  dragActive,
  setDragActive,
  fileInputRef,
  jobDescription,
  setJobDescription,
  useSampleJD,
  analyzeResume,
  loading,
  loadingStep,
  error,
}) {
  const loadingMessages = [
    "Uploading and reading your resume...",
    "Extracting technical skills...",
    "Comparing your profile with the target role...",
    "Preparing your career results...",
  ];

  return (
    <div className="page">
      <PageHeading
        eyebrow="AI RESUME ENGINE"
        title="Resume Analysis"
        description="Upload your resume and compare it against your target job description."
      />

      {error && <div className="error-message">{error}</div>}

      <div className="resume-layout">
        <section className="glass-card resume-card">
          <div className="card-header">
            <div>
              <span className="section-label">STEP 01</span>
              <h2>Upload Your Resume</h2>
              <p>PDF format • Maximum 5MB</p>
            </div>
            <div className="card-number">01</div>
          </div>

          <div
            className={`upload-box ${dragActive ? "drag-active" : ""}`}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                fileInputRef.current?.click();
              }
            }}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
            />

            <div className="upload-symbol">↑</div>

            <h3>
              {resumeFile ? resumeFile.name : "Drop your resume here"}
            </h3>

            <p>
              {resumeFile
                ? "Resume selected successfully"
                : "or click anywhere to browse your PDF"}
            </p>

            <span className="upload-hint">PDF files up to 5MB</span>
          </div>
        </section>

        <section className="glass-card">
          <div className="card-header">
            <div>
              <span className="section-label">STEP 02</span>
              <h2>Target Job Description</h2>
              <p>Tell AI what role you are targeting.</p>
            </div>

            <button className="sample-button" onClick={useSampleJD}>
              Use Sample JD
            </button>
          </div>

          <textarea
            className="job-textarea"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder={`Paste the target job description here...\n\nExample:\nWe are looking for a Python Full Stack Developer...`}
          />

          <div className="textarea-footer">
            <span>{jobDescription.length} characters</span>
            <span>AI will compare your skills automatically</span>
          </div>
        </section>

        <section className="analysis-action">
          <div>
            <div className="ready-indicator">
              <span />
              {loading ? "AI Engine Processing" : "AI Engine Ready"}
            </div>

            <h3>
              {loading
                ? loadingMessages[loadingStep] || loadingMessages[0]
                : "Ready to analyze your career fit?"}
            </h3>

            <p>
              {loading
                ? "Please wait while your resume is processed."
                : "Our analyzer will compare your resume with the target role and identify skill gaps."}
            </p>
          </div>

          <button
            className="primary-button large"
            onClick={analyzeResume}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
            {!loading && <span>→</span>}
          </button>
        </section>
      </div>
    </div>
  );
}

function SkillGap({
  analyzed,
  navigate,
  matchPercent,
  resumeSkills,
  matchedSkills,
  missingSkills,
}) {
  if (!analyzed) {
    return (
      <div className="page">
        <PageHeading
          eyebrow="SKILL INTELLIGENCE"
          title="Skill Gap Analysis"
          description="Analyze your resume first to generate your personalized skill comparison."
        />

        <div className="notice-card">
          <div className="notice-icon">!</div>
          <div>
            <h3>No resume analysis yet</h3>
            <p>Upload a resume and target job description to continue.</p>
          </div>
          <button className="primary-button" onClick={() => navigate("resume")}>
            Analyze Resume →
          </button>
        </div>
      </div>
    );
  }

  // Show every skill detected in the resume in "Your Skills".
  // Matched skills are still used by the overall match calculation from the backend.
  const displayedUserSkills = resumeSkills.length
    ? resumeSkills
    : matchedSkills;

  // Only use demo missing skills when the backend did not return any data at all.
  const safeMissing = missingSkills.length
    ? missingSkills
    : analyzed && resumeSkills.length
      ? []
      : fallbackMissingSkills;

  return (
    <div className="page">
      <PageHeading
        eyebrow="SKILL INTELLIGENCE"
        title="Skill Gap Analysis"
        description="Understand what you already know and what you need to learn for your target role."
      />

      <div className="skill-overview-grid">
        <div className="glass-card skill-score-card">
          <div className="section-label">OVERALL MATCH</div>
          <div className="big-score">
            {matchPercent}<span>%</span>
          </div>
          <p>Your current profile match based on the selected target role.</p>
          <div className="score-progress">
            <span style={{ width: `${Math.min(100, Math.max(0, matchPercent))}%` }} />
          </div>
        </div>

        <div className="glass-card">
          <div className="section-label">SKILLS FOUND</div>
          <div className="skill-count">{resumeSkills.length}</div>
          <p>Relevant skills detected in your resume.</p>
        </div>

        <div className="glass-card">
          <div className="section-label">SKILLS TO LEARN</div>
          <div className="skill-count missing-number">{safeMissing.length}</div>
          <p>Skills that can improve your job match.</p>
        </div>
      </div>

      <div className="two-column">
        <section className="glass-card">
          <div className="section-heading-row">
            <div>
              <span className="green-dot" />
              <h2>Your Skills</h2>
            </div>
            <span className="pill green">FOUND</span>
          </div>

          <div className="detailed-skills">
            {displayedUserSkills.length ? (
              displayedUserSkills.map((skill, index) => (
                <SkillProgress
                  key={typeof skill === "string" ? skill : skill.name || index}
                  name={typeof skill === "string" ? skill : skill.name}
                  level={
                    typeof skill === "string"
                      ? 100
                      : Number.isFinite(Number(skill.level))
                        ? Number(skill.level)
                        : 100
                  }
                  type="strong"
                />
              ))
            ) : (
              <p className="muted">No skills were detected from the resume.</p>
            )}
          </div>
        </section>

        <section className="glass-card">
          <div className="section-heading-row">
            <div>
              <span className="red-dot" />
              <h2>Skills To Learn</h2>
            </div>
            <span className="pill red">PRIORITY</span>
          </div>

          <div className="missing-skill-list">
            {safeMissing.map((skill, index) => (
              <MissingSkill
                key={skill.name || index}
                name={skill.name}
                priority={skill.priority || "Medium"}
                progress={skill.progress || 0}
              />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function SkillProgress({ name, level, type }) {
  return (
    <div className="skill-progress-item">
      <div className="skill-progress-top">
        <span>{name}</span>
        <strong>{level}%</strong>
      </div>
      <div className="skill-track">
        <span className={type} style={{ width: `${level}%` }} />
      </div>
    </div>
  );
}

function MissingSkill({ name, priority, progress }) {
  return (
    <div className="missing-skill">
      <div className="missing-skill-top">
        <div>
          <strong>{name}</strong>
          <span className={`priority ${priority.toLowerCase()}`}>
            {priority}
          </span>
        </div>
        <span>{progress}%</span>
      </div>

      <div className="skill-track">
        <span className="missing-track" style={{ width: `${progress}%` }} />
      </div>
    </div>
  );
}

function JobMatches({
  jobs,
  search,
  setSearch,
  jobSort,
  setJobSort,
  jobFilter,
  setJobFilter,
  jobCategory,
  setJobCategory,
  selectJob,
  analyzed,
}) {
  return (
    <div className="page">
      <PageHeading
        eyebrow="CAREER OPPORTUNITIES"
        title="Job Matches"
        description="Explore roles that match your current skills and career profile."
      />

      {!analyzed && (
        <div className="notice-card">
          <div className="notice-icon">!</div>
          <div>
            <h3>Showing example job matches</h3>
            <p>Analyze your resume to generate personalized recommendations.</p>
          </div>
        </div>
      )}

      <div className="job-toolbar">
        <div className="search-box">
          <span>⌕</span>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search jobs, companies or locations..."
          />
        </div>

        <select
          className="filter-button"
          value={jobCategory}
          onChange={(e) => setJobCategory(e.target.value)}
          aria-label="Filter job category"
        >
          <option value="all">All Categories</option>
          <option value="IT & Software">IT & Software</option>
          <option value="Data & Analytics">Data & Analytics</option>
          <option value="AI & ML">AI & ML</option>
          <option value="Cloud & DevOps">Cloud & DevOps</option>
          <option value="Testing & QA">Testing & QA</option>
          <option value="IT Support">IT Support</option>
          <option value="BPO & Customer Support">BPO & Customer Support</option>
          <option value="Sales & Business">Sales & Business</option>
          <option value="HR & Administration">HR & Administration</option>
        </select>

        <select
          className="filter-button"
          value={jobFilter}
          onChange={(e) => setJobFilter(e.target.value)}
          aria-label="Filter job matches"
        >
          <option value="all">All Matches</option>
          <option value="80">80%+ Match</option>
          <option value="60">60%+ Match</option>
        </select>

        <select
          className="filter-button"
          value={jobSort}
          onChange={(e) => setJobSort(e.target.value)}
          aria-label="Sort job matches"
        >
          <option value="high-low">High to Low</option>
          <option value="low-high">Low to High</option>
        </select>
      </div>

      <div className="job-result-info">
        <span>
          <strong>{jobs.length}</strong> matching opportunities
        </span>
        <span>
          {jobCategory === "all" ? "All career categories" : jobCategory} • Sorted by skill match
        </span>
      </div>

      <div className="job-grid-modern">
        {jobs.map((job) => (
          <JobCard
            key={`${job.title}-${job.company}`}
            job={job}
            onSelect={selectJob}
          />
        ))}

        {!jobs.length && (
          <div className="empty-state">No matching jobs found.</div>
        )}
      </div>
    </div>
  );
}

function JobCard({ job, onSelect }) {
  return (
    <article className="modern-job-card">
      <div className="job-card-top">
        <div className="company-logo">
          {(job.company || "R").charAt(0)}
        </div>
        <span className="match-badge">
          {job.match_percentage}% Match
        </span>
      </div>

      <h3>{job.title}</h3>
      <p className="company-name">{job.company}</p>
      <p className="job-location">◉ {job.location}</p>

      <div className="job-meta">
        <span>{job.category || getJobCategory(job.title)}</span>
        <span>{job.experience || "Fresher / Entry Level"}</span>
        <span>{job.work_mode || "Full-time"}</span>
      </div>

      <div className="job-skills">
        {(Array.isArray(job.required_skills) ? job.required_skills : [])
          .slice(0, 5)
          .map((skill) => (
            <span key={skill}>{skill}</span>
          ))}
      </div>

      <button className="job-button" onClick={() => onSelect(job)}>
        View Roadmap →
      </button>
    </article>
  );
}

function LearningRoadmap({
  roadmap,
  selectedJob,
  openRoadmap,
  setOpenRoadmap,
  completedTopics,
  toggleTopic,
  roadmapProgress,
}) {
  return (
    <div className="page">
      <PageHeading
        eyebrow="PERSONALIZED LEARNING"
        title={
          selectedJob && Number(selectedJob.match_percentage || 0) >= 100
            ? "Advanced Career Roadmap"
            : "Learning Roadmap"
        }
        description={
          selectedJob && Number(selectedJob.match_percentage || 0) >= 100
            ? "You already match the core skills for this role. Continue with advanced topics and production-level projects."
            : "Follow a structured path from your current skills to your target career."
        }
      />

      <div className="roadmap-summary">
        <div className="roadmap-summary-main">
          <div className="roadmap-icon">◇</div>
          <div>
            <span className="section-label">YOUR CAREER PATH</span>
            <h2>{selectedJob?.title || "Full Stack Developer"}</h2>
            <p>
              {selectedJob
                ? Number(selectedJob.match_percentage || 0) >= 100
                  ? "100% core skill match • Advanced learning path"
                  : `${selectedJob.match_percentage}% current skill match`
                : "Complete an analysis to personalize this roadmap."}
            </p>
          </div>
        </div>

        <div className="roadmap-completion">
          <strong>{roadmapProgress}%</strong>
          <span>Completed</span>
          <div>
            <span style={{ width: `${roadmapProgress}%` }} />
          </div>
        </div>
      </div>

      <div className="timeline">
        {roadmap.map((item, index) => {
          const isOpen = openRoadmap === index;

          return (
            <div
              className={`timeline-item ${isOpen ? "open" : ""}`}
              key={`${item.number}-${item.title}`}
            >
              <div className="timeline-line" />

              <button
                className="timeline-number"
                onClick={() => setOpenRoadmap(isOpen ? -1 : index)}
                aria-label={`Open ${item.title}`}
              >
                {item.number}
              </button>

              <div className="timeline-card">
                <button
                  className="timeline-header"
                  onClick={() => setOpenRoadmap(isOpen ? -1 : index)}
                  aria-expanded={isOpen}
                >
                  <div>
                    <span className="step-label">STEP {item.number}</span>
                    <h3>{item.title}</h3>
                    <p>{item.duration}</p>
                  </div>
                  <span className="expand-icon">{isOpen ? "−" : "+"}</span>
                </button>

                {isOpen && (
                  <div className="timeline-content">
                    <p>{item.description}</p>

                    <div className="topic-grid">
                      {item.topics.length ? (
                        item.topics.map((topic, topicIndex) => {
                          const key = `${index}-${topicIndex}`;
                          return (
                            <label key={topic}>
                              <input
                                type="checkbox"
                                checked={Boolean(completedTopics[key])}
                                onChange={() => toggleTopic(index, topicIndex)}
                              />
                              <span>{topic}</span>
                            </label>
                          );
                        })
                      ) : (
                        <span className="muted">
                          No topic list returned by the roadmap service.
                        </span>
                      )}
                    </div>

                    <div className="free-resource-box">
                      <div className="resource-icon">📚</div>
                      <div className="resource-content">
                        <h4>Free Learning Resource</h4>
                        <p>
                          Learn {item.title} using a free learning resource.
                        </p>

                        {item.resource ? (
                          <a
                            href={item.resource}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="resource-button"
                          >
                            Start Learning Free →
                          </a>
                        ) : (
                          <a
                            href={`https://www.google.com/search?q=${encodeURIComponent(
                              `${item.title} free course`
                            )}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="resource-button"
                          >
                            Find Free Course →
                          </a>
                        )}
                      </div>
                    </div>

                    <div className="mini-project">
                      <h4>🛠️ Mini Project</h4>
                      <p>
                        {item.project ||
                          `Build a ${item.title}-based mini project to practice what you learned.`}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function JobModal({ job, onClose }) {
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="job-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close">
          ×
        </button>
        <h2>{job.title}</h2>
        <p>{job.company} • {job.location}</p>
        <div className="modal-section">
          <strong>Match</strong>
          <div className="modal-match">{job.match_percentage}%</div>
        </div>
      </div>
    </div>
  );
}

function PageHeading({ eyebrow, title, description }) {
  return (
    <div className="page-heading">
      <span className="page-eyebrow">✦ {eyebrow}</span>
      <h1>{title}</h1>
      <p>{description}</p>
    </div>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-brand">✦ CareerForge AI</div>
      <p>AI-powered career analysis • Analyze • Match • Grow</p>
      <span>© 2026 CareerForge AI</span>
    </footer>
  );
}

export default App;
