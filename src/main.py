from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.agents.pipeline import CourtPipeline

load_dotenv()

app = FastAPI(
    title="AI Judge API",
    description="Backend API for AI-based dramatic judgment application",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = CourtPipeline(model="llama-3.1-8b-instant")

# ── Request/Response models ───────────────────────────────────────────────────

class StartCaseRequest(BaseModel):
    situation: str = Field(..., max_length=1000, min_length=1)

    @validator('situation')
    def validate_situation(cls, v):
        if not v.strip():
            raise ValueError('Situation cannot be empty')
        return v.strip()


class AnswerRequest(BaseModel):
    session_id: str
    answer: str = Field(..., min_length=1)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "AI Judge API is running", "status": "healthy", "version": "2.0.0"}


@app.post("/api/v1/start")
async def start_case(request: StartCaseRequest):
    """
    Începe un caz nou. Returnează fie o întrebare de clarificare,
    fie direct verdictul dacă situația e suficient de detaliată.

    Response:
        state == "question" → frontend afișează întrebarea și un input
        state == "verdict"  → frontend afișează verdictul
    """
    result = pipeline.start_case(request.situation)

    if result.get("state") == "error":
        raise HTTPException(status_code=503, detail=result.get("error"))

    return result


@app.post("/api/v1/answer")
async def answer_question(request: AnswerRequest):
    """
    Trimite răspunsul utilizatorului la întrebarea curentă.
    Returnează fie următoarea întrebare, fie verdictul final.
    """
    result = pipeline.answer_question(request.session_id, request.answer)

    if result.get("state") == "error":
        raise HTTPException(status_code=503, detail=result.get("error"))

    return result


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )
