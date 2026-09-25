from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.resume import router as resume_router
from routes.analysis import router as analysis_router
from routes.jobs import router as jobs_router


app = FastAPI()


# ---------------------------------------------------
# CORS Configuration
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Home
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Job Skill Analyzer API is running"
    }


# ---------------------------------------------------
# Routers
# ---------------------------------------------------

app.include_router(
    resume_router,
    prefix="/api"
)

app.include_router(
    analysis_router,
    prefix="/api"
)

app.include_router(jobs_router, prefix="/api")