from fastapi import FastAPI
from routers import resume, interview, summary

app = FastAPI(title="AI Candidate Screening System")

app.include_router(resume.router, prefix="/resume")
app.include_router(interview.router, prefix="/interview")
app.include_router(summary.router, prefix="/summary")
