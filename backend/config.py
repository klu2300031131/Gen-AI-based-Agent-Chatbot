"""
KLU Agent - Configuration Module
Manages all environment variables and application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# ============================================
# LLM Configuration
# ============================================
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" or "openai"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model names
GEMINI_MODEL = "gemini-2.0-flash"
OPENAI_MODEL = "gpt-3.5-turbo"

# ============================================
# Embedding Configuration
# ============================================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ============================================
# ChromaDB Configuration
# ============================================
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))
CHROMA_COLLECTION_NAME = "klu_knowledge"

# ============================================
# Database Configuration
# ============================================
DATABASE_URL = f"sqlite:///{BASE_DIR / 'klu_college.db'}"

# ============================================
# Document Storage
# ============================================
DOCUMENTS_DIR = str(BASE_DIR / "data" / "documents")

# ============================================
# Server Configuration
# ============================================
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# ============================================
# RAG Configuration
# ============================================
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5
TEMPERATURE = 0.3
