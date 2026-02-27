# ============================================================
#  KLU Smart Assistant — Central Configuration
#  Agentic RAG Framework Settings
# ============================================================

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Project Paths ─────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent
DOCS_DIR  = BASE_DIR / "docs"
DB_DIR    = BASE_DIR / "vector_db"
LOG_DIR   = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"

for d in [DOCS_DIR, DB_DIR, LOG_DIR, MODEL_DIR]:
    d.mkdir(exist_ok=True)

# ── LLM Configuration ─────────────────────────────────────
LLM_CONFIG = {
    # Primary: OpenAI GPT-4o (via API key)
    "openai": {
        "provider"   : "openai",
        "model"      : "gpt-4o",
        "api_key"    : os.getenv("OPENAI_API_KEY", ""),
        "temperature": 0.2,
        "max_tokens" : 1024,
        "top_p"      : 0.95,
        "timeout"    : 30,
    },
    # Fallback: Local Ollama (Llama 3.1 8B)
    "ollama": {
        "provider"   : "ollama",
        "model"      : "llama3.1:8b",
        "base_url"   : "http://localhost:11434",
        "temperature": 0.1,
        "max_tokens" : 1024,
    },
    # Fallback 2: HuggingFace Mistral-7B
    "huggingface": {
        "provider"  : "huggingface",
        "model"     : "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "api_token" : os.getenv("HF_API_TOKEN", ""),
        "task"      : "text-generation",
    },
    "active": "ollama",   # Switch between "openai" / "ollama" / "huggingface"
}

# ── Embedding Model ────────────────────────────────────────
EMBEDDING_CONFIG = {
    "model_name"  : "sentence-transformers/all-MiniLM-L6-v2",
    "device"      : "cpu",                  # "cuda" if GPU available
    "batch_size"  : 64,
    "normalize"   : True,
    "cache_dir"   : str(MODEL_DIR / "embeddings"),
    "dimension"   : 384,                    # all-MiniLM-L6-v2 output dim
}

# ── Vector Store (ChromaDB) ────────────────────────────────
CHROMA_CONFIG = {
    "persist_directory" : str(DB_DIR / "chroma"),
    "collection_name"   : "klu_knowledge_base",
    "distance_function" : "cosine",
    "top_k"             : 8,
    "score_threshold"   : 0.45,
}

# ── FAISS Fallback Index ───────────────────────────────────
FAISS_CONFIG = {
    "index_path"  : str(DB_DIR / "faiss_index.bin"),
    "metadata_path": str(DB_DIR / "faiss_metadata.pkl"),
    "index_type"  : "IndexFlatIP",   # Inner Product (cosine after normalise)
    "top_k"       : 8,
}

# ── College Database (MySQL) ───────────────────────────────
DB_CONFIG = {
    "host"    : os.getenv("DB_HOST", "localhost"),
    "port"    : int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "klu_university_db"),
    "user"    : os.getenv("DB_USER", "klu_admin"),
    "password": os.getenv("DB_PASSWORD", ""),
    "pool_size": 5,
    "timeout" : 30,
}

# ── Document Processing ────────────────────────────────────
DOCUMENT_CONFIG = {
    "chunk_size"   : 512,
    "chunk_overlap": 64,
    "separators"   : ["\n\n", "\n", ". ", " "],
    "supported_ext": [".pdf", ".txt", ".docx", ".md", ".json"],
    "docs_path"    : str(DOCS_DIR),
}

# ── Agent Settings ─────────────────────────────────────────
AGENT_CONFIG = {
    "agent_type"       : "ReAct",        # Reasoning + Acting
    "max_iterations"   : 6,
    "max_exec_time"    : 20,
    "verbose"          : True,
    "return_direct"    : False,
    "handle_errors"    : True,
    "memory_window"    : 10,             # chat history turns to keep
    "system_prompt"    : (
        "You are KLU Smart Assistant, an expert AI guide for KL University. "
        "Answer questions accurately using the retrieved context from documents "
        "and the university database. Be concise, friendly, and student-focused. "
        "If you are unsure, say so clearly — never hallucinate."
    ),
}

# ── API Server ─────────────────────────────────────────────
API_CONFIG = {
    "host"        : "0.0.0.0",
    "port"        : 5000,
    "debug"       : False,
    "reload"      : True,
    "workers"     : 4,
    "cors_origins": ["*"],
    "rate_limit"  : "60/minute",
}

# ── Logging ────────────────────────────────────────────────
LOG_CONFIG = {
    "level"  : "INFO",
    "file"   : str(LOG_DIR / "klu_agent.log"),
    "rotate" : "10 MB",
    "retain" : "7 days",
    "format" : "{time} | {level} | {name} — {message}",
}
