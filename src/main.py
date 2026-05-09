from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="AI Judge API",
    description="Backend API for AI-based dramatic judgment application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ComplaintRequest(BaseModel):
    situation: str = Field(
        ..., 
        max_length=1000,
        min_length=1,
        description="Description of the situation to be judged"
    )
    
    @validator('situation')
    def validate_situation(cls, v):
        if not v.strip():
            raise ValueError('Situation cannot be empty or whitespace only')
        return v.strip()

class JudgmentResponse(BaseModel):
    case_title: str
    charges: str
    evidence_presented: str
    legal_precedent: str
    verdict: str
    sentence: str
    legal_reasoning: str
    courts_final_words: str

@app.get("/")
async def root():
    return {
        "message": "AI Judge API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/api/v1/judge", response_model=JudgmentResponse, status_code=200)
async def get_judgment(complaint: ComplaintRequest):

    dummy_response = JudgmentResponse(
        case_title=f"The Case of the {complaint.situation[:30]}...",
        charges="Placeholder charges - LLM integration pending",
        evidence_presented="Placeholder evidence - LLM integration pending",
        legal_precedent="Placeholder precedent - LLM integration pending",
        verdict="PENDING - Awaiting LLM Integration",
        sentence="Placeholder sentence - LLM integration pending",
        legal_reasoning="Placeholder reasoning - LLM integration pending",
        courts_final_words="This court will reconvene once the AI judge is properly installed!"
    )
    
    return dummy_response

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }