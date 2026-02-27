# ============================================================
#  KLU Smart Assistant — Embedding Engine
#  HuggingFace Sentence-Transformers
#  Converts text → dense vector representations
# ============================================================

import time
import logging
import numpy as np
from typing import List, Union
from pathlib import Path

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from config import EMBEDDING_CONFIG

logger = logging.getLogger("KLU.Embeddings")


class EmbeddingEngine:
    """
    Wraps HuggingFace sentence-transformer model.
    Supports single strings and batch encoding.
    Model: sentence-transformers/all-MiniLM-L6-v2 (384-dim)
    """

    def __init__(self):
        self.model_name  = EMBEDDING_CONFIG["model_name"]
        self.device      = EMBEDDING_CONFIG["device"]
        self.batch_size  = EMBEDDING_CONFIG["batch_size"]
        self.normalize   = EMBEDDING_CONFIG["normalize"]
        self.dimension   = EMBEDDING_CONFIG["dimension"]
        self.model       = None
        self.tokenizer   = None
        self._load_model()

    def _load_model(self):
        logger.info(f"⬇️  Loading embedding model: {self.model_name} → device={self.device}")
        t0 = time.time()

        self.model = SentenceTransformer(
            self.model_name,
            device     = self.device,
            cache_folder = EMBEDDING_CONFIG["cache_dir"],
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            cache_dir = EMBEDDING_CONFIG["cache_dir"],
        )

        load_time = time.time() - t0
        logger.info(
            f"✅ Embedding model loaded in {load_time:.2f}s | "
            f"dim={self.dimension} | device={self.device}"
        )

    def encode(
        self,
        texts: Union[str, List[str]],
        show_progress: bool = False,
    ) -> np.ndarray:
        """
        Encode one or more texts into dense vectors.
        Returns shape (N, embedding_dim).
        """
        if isinstance(texts, str):
            texts = [texts]

        logger.debug(f"🔢 Encoding {len(texts)} text(s)...")
        t0 = time.time()

        embeddings = self.model.encode(
            texts,
            batch_size          = self.batch_size,
            normalize_embeddings = self.normalize,
            show_progress_bar   = show_progress,
            convert_to_numpy    = True,
        )

        elapsed = time.time() - t0
        logger.debug(
            f"✅ Encoded {len(texts)} texts in {elapsed*1000:.1f}ms | "
            f"shape={embeddings.shape}"
        )
        return embeddings

    def encode_query(self, query: str) -> np.ndarray:
        """Encode a single search query. Returns shape (1, dim)."""
        return self.encode([query])

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        a = a / (np.linalg.norm(a) + 1e-10)
        b = b / (np.linalg.norm(b) + 1e-10)
        return float(np.dot(a, b))

    def batch_cosine_similarity(
        self, query: np.ndarray, corpus: np.ndarray
    ) -> np.ndarray:
        """
        Compute cosine similarity between one query and many corpus vectors.
        Returns array of shape (N,).
        """
        query  = query  / (np.linalg.norm(query,  axis=-1, keepdims=True) + 1e-10)
        corpus = corpus / (np.linalg.norm(corpus, axis=-1, keepdims=True) + 1e-10)
        return (corpus @ query.T).squeeze()

    def token_count(self, text: str) -> int:
        """Returns token count for a given text."""
        return len(self.tokenizer.encode(text, truncation=False))

    @property
    def max_seq_length(self) -> int:
        return self.model.max_seq_length

    def __repr__(self):
        return (
            f"EmbeddingEngine("
            f"model={self.model_name}, "
            f"dim={self.dimension}, "
            f"device={self.device})"
        )
