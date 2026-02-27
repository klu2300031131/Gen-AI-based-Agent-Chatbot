# ============================================================
#  KLU Smart Assistant — Vector Store Manager
#  ChromaDB (primary) + FAISS (fallback)
#  Stores and retrieves document embeddings for RAG pipeline
# ============================================================

import os
import pickle
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import faiss

from config import CHROMA_CONFIG, FAISS_CONFIG, EMBEDDING_CONFIG

logger = logging.getLogger("KLU.VectorStore")


# ============================================================
#  CHROMA VECTOR STORE
# ============================================================

class ChromaVectorStore:
    """
    ChromaDB-backed vector store for document retrieval.
    Persists embeddings to disk for fast subsequent loading.
    """

    def __init__(self):
        self.client     = None
        self.collection = None
        self._init_client()

    def _init_client(self):
        logger.info(f"🗄️  Initialising ChromaDB client at: {CHROMA_CONFIG['persist_directory']}")
        self.client = chromadb.PersistentClient(
            path=CHROMA_CONFIG["persist_directory"],
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        # Use HuggingFace sentence-transformer as embedding fn
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name  = EMBEDDING_CONFIG["model_name"],
            device      = EMBEDDING_CONFIG["device"],
            normalize_embeddings = EMBEDDING_CONFIG["normalize"],
        )

        self.collection = self.client.get_or_create_collection(
            name     = CHROMA_CONFIG["collection_name"],
            metadata = {"hnsw:space": CHROMA_CONFIG["distance_function"]},
            embedding_function = ef,
        )
        logger.info(f"✅ ChromaDB collection '{CHROMA_CONFIG['collection_name']}' ready "
                    f"— {self.collection.count()} documents indexed")

    def add_documents(self, docs: List[Dict]) -> int:
        """
        Add chunked documents to the vector store.
        Each doc must have: {'id', 'text', 'metadata'}
        """
        if not docs:
            logger.warning("No documents provided to index.")
            return 0

        ids       = [d["id"]       for d in docs]
        texts     = [d["text"]     for d in docs]
        metadatas = [d["metadata"] for d in docs]

        logger.info(f"📥 Indexing {len(docs)} document chunks into ChromaDB...")
        batch_size = 100
        for i in range(0, len(docs), batch_size):
            self.collection.add(
                ids       = ids[i:i+batch_size],
                documents = texts[i:i+batch_size],
                metadatas = metadatas[i:i+batch_size],
            )
            logger.debug(f"   Batch {i//batch_size + 1} indexed.")

        logger.info(f"✅ Indexed {len(docs)} chunks — total: {self.collection.count()}")
        return len(docs)

    def query(self, query_text: str, top_k: int = None) -> List[Dict]:
        """
        Semantic search: returns top-k most relevant document chunks.
        """
        k = top_k or CHROMA_CONFIG["top_k"]
        logger.debug(f"🔍 Querying ChromaDB — top_k={k} | query: '{query_text[:60]}...'")

        results = self.collection.query(
            query_texts      = [query_text],
            n_results        = k,
            include          = ["documents", "metadatas", "distances"],
        )

        hits = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = 1 - dist   # convert distance → similarity
            if score >= CHROMA_CONFIG["score_threshold"]:
                hits.append({
                    "text"    : doc,
                    "metadata": meta,
                    "score"   : round(score, 4),
                    "source"  : "chroma",
                })

        logger.info(f"📊 ChromaDB returned {len(hits)} relevant chunks "
                    f"(threshold ≥ {CHROMA_CONFIG['score_threshold']})")
        return hits

    def delete_collection(self):
        self.client.delete_collection(CHROMA_CONFIG["collection_name"])
        logger.warning("⚠️  ChromaDB collection deleted and reset.")

    def count(self) -> int:
        return self.collection.count()


# ============================================================
#  FAISS VECTOR STORE (Fallback / High-speed index)
# ============================================================

class FAISSVectorStore:
    """
    FAISS-backed in-memory vector store.
    Used as high-speed fallback when ChromaDB is unavailable,
    or for large-scale ANN search benchmarking.
    """

    def __init__(self, dim: int = EMBEDDING_CONFIG["dimension"]):
        self.dim      = dim
        self.index    = None
        self.metadata = []      # parallel list to FAISS index rows
        self._build_index()
        logger.info(f"⚡ FAISS index initialised — type: {FAISS_CONFIG['index_type']} "
                    f"| dim: {self.dim}")

    def _build_index(self):
        if FAISS_CONFIG["index_type"] == "IndexFlatIP":
            self.index = faiss.IndexFlatIP(self.dim)
        elif FAISS_CONFIG["index_type"] == "IndexFlatL2":
            self.index = faiss.IndexFlatL2(self.dim)
        else:
            # IVF index for large-scale (>100k vectors)
            quantizer  = faiss.IndexFlatIP(self.dim)
            self.index = faiss.IndexIVFFlat(quantizer, self.dim, 100)

    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]):
        """Add pre-computed embedding vectors to the FAISS index."""
        if embeddings.shape[1] != self.dim:
            raise ValueError(f"Embedding dim mismatch: got {embeddings.shape[1]}, expected {self.dim}")

        # Normalise for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype(np.float32))
        self.metadata.extend(metadata)
        logger.info(f"📥 Added {len(metadata)} vectors to FAISS — "
                    f"total: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, top_k: int = None) -> List[Dict]:
        """Approximate nearest neighbour search."""
        k = top_k or FAISS_CONFIG["top_k"]

        if self.index.ntotal == 0:
            logger.warning("FAISS index is empty. No results.")
            return []

        query = query_embedding.astype(np.float32).reshape(1, -1)
        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, k)

        hits = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and score > 0.4:
                hits.append({
                    **self.metadata[idx],
                    "score" : round(float(score), 4),
                    "source": "faiss",
                })

        logger.info(f"⚡ FAISS returned {len(hits)} results for top_k={k}")
        return hits

    def save(self):
        faiss.write_index(self.index, FAISS_CONFIG["index_path"])
        with open(FAISS_CONFIG["metadata_path"], "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info(f"💾 FAISS index saved → {FAISS_CONFIG['index_path']}")

    def load(self):
        if Path(FAISS_CONFIG["index_path"]).exists():
            self.index    = faiss.read_index(FAISS_CONFIG["index_path"])
            with open(FAISS_CONFIG["metadata_path"], "rb") as f:
                self.metadata = pickle.load(f)
            logger.info(f"📂 FAISS index loaded — {self.index.ntotal} vectors")
        else:
            logger.warning("No saved FAISS index found. Starting fresh.")


# ============================================================
#  UNIFIED RETRIEVER (ChromaDB + FAISS Hybrid)
# ============================================================

class HybridRetriever:
    """
    Combines ChromaDB semantic search with FAISS ANN search.
    Results are de-duplicated and re-ranked by score.
    """

    def __init__(self):
        logger.info("🔀 Initialising HybridRetriever (ChromaDB + FAISS)...")
        self.chroma = ChromaVectorStore()
        self.faiss  = FAISSVectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 6,
        use_faiss: bool = False,
        embedding: Optional[np.ndarray] = None,
    ) -> List[Dict]:

        results = self.chroma.query(query, top_k=top_k)

        if use_faiss and embedding is not None:
            faiss_results = self.faiss.search(embedding, top_k=top_k)
            results.extend(faiss_results)

        # De-duplicate based on text hash
        seen   = set()
        unique = []
        for r in results:
            key = hash(r["text"][:100])
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # Re-rank by score (descending)
        unique.sort(key=lambda x: x["score"], reverse=True)

        logger.info(f"✅ HybridRetriever: {len(unique)} unique chunks retrieved")
        return unique[:top_k]
