"""
KLU Agent - FastAPI Main Application
RESTful API server for the KLU Agent chatbot.
"""

import sys
import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List

# Add parent dir to path
sys.path.insert(0, os.path.dirname(__file__))

import config
from data.database import init_db, seed_db, SessionLocal, Event, FAQ


# ============================================
# Pydantic Models
# ============================================

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for context")


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    tools_used: List[str]
    response_time: float


class HealthResponse(BaseModel):
    status: str
    llm_provider: str
    vector_store: str
    database: str


# ============================================
# Application Lifespan
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, cleanup on shutdown."""
    print("Starting KLU Agent Backend...")

    # Initialize database (fast - keep synchronous)
    print("Initializing database...")
    init_db()
    seed_db()
    print("Database ready!")

    # Initialize vector store in background thread (slow - don't block startup)
    import threading
    def _init_rag():
        try:
            print("Initializing RAG pipeline in background...")
            from rag.vector_store import get_vector_store
            store = get_vector_store()
            if store:
                print("Vector store ready!")
            else:
                print("Vector store initialization failed - will retry on first query")
        except Exception as e:
            print(f"Vector store pre-loading failed: {e}")

    threading.Thread(target=_init_rag, daemon=True).start()

    print("KLU Agent Backend is ready!")
    print(f"API running at http://localhost:{config.PORT}")
    print(f"LLM Provider: {config.LLM_PROVIDER}")

    yield

    print("Shutting down KLU Agent Backend...")


# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="KLU Agent API",
    description="Gen AI-powered Agent Chatbot for KL University",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
if os.path.exists(os.path.join(frontend_dir, "index.html")):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# ============================================
# API Endpoints
# ============================================

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML page."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "KLU Agent API is running. Frontend not found at expected location."}


@app.get("/styles.css", response_class=FileResponse)
async def serve_css():
    """Serve the frontend CSS file."""
    return FileResponse(os.path.join(frontend_dir, "styles.css"), media_type="text/css")


@app.get("/app.js", response_class=FileResponse)
async def serve_js():
    """Serve the frontend JS file."""
    return FileResponse(os.path.join(frontend_dir, "app.js"), media_type="application/javascript")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of all system components."""
    # Check database
    db_status = "healthy"
    try:
        session = SessionLocal()
        session.execute(
            __import__('sqlalchemy').text("SELECT 1")
        )
        session.close()
    except Exception:
        db_status = "unhealthy"

    # Check vector store
    vs_status = "not initialized"
    try:
        from rag.vector_store import _vector_store
        if _vector_store is not None:
            count = _vector_store._collection.count()
            vs_status = f"healthy ({count} documents)"
    except Exception:
        vs_status = "error"

    return HealthResponse(
        status="running",
        llm_provider=config.LLM_PROVIDER,
        vector_store=vs_status,
        database=db_status
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Sends user message to the KLU Agent
    and returns a grounded response.
    """
    start_time = time.time()

    # Validate API key is configured
    if config.LLM_PROVIDER == "gemini" and not config.GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Google API key not configured. Please set GOOGLE_API_KEY in the .env file."
        )
    elif config.LLM_PROVIDER == "openai" and not config.OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in the .env file."
        )

    try:
        from agents.klu_agent import run_agent
        result = run_agent(request.message)

        response_time = round(time.time() - start_time, 2)

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            tools_used=result["tools_used"],
            response_time=response_time
        )

    except Exception as e:
        print(f"❌ Chat error: {e}")
        response_time = round(time.time() - start_time, 2)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.get("/api/events")
async def get_events():
    """Get all upcoming events."""
    session = SessionLocal()
    try:
        events = session.query(Event).filter(Event.is_upcoming == True).all()
        return [{
            "id": e.id,
            "name": e.name,
            "type": e.event_type,
            "description": e.description,
            "date": e.date,
            "venue": e.venue
        } for e in events]
    finally:
        session.close()


@app.get("/api/faqs")
async def get_faqs(category: Optional[str] = None):
    """Get FAQs, optionally filtered by category."""
    session = SessionLocal()
    try:
        query = session.query(FAQ)
        if category:
            query = query.filter(FAQ.category == category)
        faqs = query.all()
        return [{
            "id": f.id,
            "question": f.question,
            "answer": f.answer,
            "category": f.category
        } for f in faqs]
    finally:
        session.close()


@app.post("/api/rebuild-index")
async def rebuild_index():
    """Rebuild the vector store index from scratch."""
    try:
        from rag.vector_store import initialize_vector_store
        store = initialize_vector_store()
        if store:
            count = store._collection.count()
            return {"status": "success", "documents_indexed": count}
        return {"status": "failed", "message": "Could not initialize vector store"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Run Server
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="info"
    )
