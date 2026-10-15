from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.graph import ask_question


app = FastAPI(
    title="Pakistani Law RAG Chatbot",
    description="AI chatbot for Pakistani Law",
    version="1.0.0"
)


# Frontend HTML file ka path
BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "frontend" / "index.html"


# Home page: frontend show karega
@app.get("/", include_in_schema=False)
def home():
    if not INDEX_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="index.html file not found. Check app/frontend/index.html"
        )

    return FileResponse(INDEX_FILE)


# API health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Question request format
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


# User ke question ka answer
@app.post("/ask")
def ask_law_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:
        result = ask_question(question)

        return {
            "question": question,
            "answer": result.get("answer", ""),
            "is_in_scope": result.get("is_in_scope", False),
            "sources": result.get("sources", []),
            "retrieval_time_ms": result.get("retrieval_time_ms", 0.0),
            "generation_time_ms": result.get("generation_time_ms", 0.0)
        }

    except Exception as error:
        print(f"Error generating answer: {error}")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the answer."
        ) from error