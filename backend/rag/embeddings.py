"""
KLU Agent - Embedding Module
Handles text embedding using HuggingFace sentence-transformers.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
import config


_embedding_model = None


def get_embedding_model():
    """
    Get or create the embedding model (singleton pattern).
    Uses HuggingFace sentence-transformers for generating embeddings.
    """
    global _embedding_model

    if _embedding_model is None:
        print(f"🔄 Loading embedding model: {config.EMBEDDING_MODEL}...")
        _embedding_model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        print(f"✅ Embedding model loaded: {config.EMBEDDING_MODEL}")

    return _embedding_model
