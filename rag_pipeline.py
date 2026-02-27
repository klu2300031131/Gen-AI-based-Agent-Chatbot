# ============================================================
#  KLU Smart Assistant — RAG Pipeline
#  Retrieval-Augmented Generation with LangChain
#
#  Flow:
#    User Query
#      → Embed Query (sentence-transformers)
#      → Retrieve Chunks (ChromaDB / FAISS)
#      → Retrieve DB Records (MySQL)
#      → Merge Context
#      → Generate Answer (LLM: GPT-4o / Llama3 / Mixtral)
#      → Return Response
# ============================================================

import time
import logging
from typing import List, Dict, Any, Optional

from langchain.schema          import Document
from langchain.prompts         import PromptTemplate, ChatPromptTemplate
from langchain.memory          import ConversationBufferWindowMemory
from langchain.chains          import RetrievalQAWithSourcesChain, LLMChain
from langchain.text_splitter   import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader,
    JSONLoader, DirectoryLoader,
)
from langchain_community.llms        import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings   import HuggingFaceEmbeddings

from config       import (DOCUMENT_CONFIG, LLM_CONFIG, AGENT_CONFIG,
                           CHROMA_CONFIG, EMBEDDING_CONFIG, DOCS_DIR)
from embeddings   import EmbeddingEngine
from vector_store import HybridRetriever
from database     import UniversityDB

logger = logging.getLogger("KLU.RAGPipeline")


# ============================================================
#  DOCUMENT INGESTION
# ============================================================

class DocumentIngester:
    """
    Loads documents from DOCS_DIR, splits into chunks,
    and indexes them into the vector store.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size    = DOCUMENT_CONFIG["chunk_size"],
            chunk_overlap = DOCUMENT_CONFIG["chunk_overlap"],
            separators    = DOCUMENT_CONFIG["separators"],
        )
        logger.info(
            f"📄 DocumentIngester ready | "
            f"chunk_size={DOCUMENT_CONFIG['chunk_size']} | "
            f"overlap={DOCUMENT_CONFIG['chunk_overlap']}"
        )

    def load_directory(self, path: str = None) -> List[Document]:
        doc_path = path or str(DOCS_DIR)
        logger.info(f"📂 Loading documents from: {doc_path}")

        loader = DirectoryLoader(
            doc_path,
            glob        = "**/*.*",
            show_progress = True,
            use_multithreading = True,
        )
        raw_docs = loader.load()
        logger.info(f"✅ Loaded {len(raw_docs)} raw document pages")
        return raw_docs

    def split(self, docs: List[Document]) -> List[Document]:
        logger.info(f"✂️  Splitting {len(docs)} docs into chunks...")
        chunks = self.splitter.split_documents(docs)
        logger.info(f"✅ Created {len(chunks)} chunks")
        return chunks

    def ingest(self, path: str = None) -> int:
        """Full ingestion pipeline: load → split → return chunks."""
        raw   = self.load_directory(path)
        chunks = self.split(raw)
        return chunks


# ============================================================
#  LLM FACTORY
# ============================================================

class LLMFactory:
    """Creates the correct LLM based on config."""

    @staticmethod
    def build():
        provider = LLM_CONFIG["active"]
        cfg      = LLM_CONFIG[provider]
        logger.info(f"🤖 Initialising LLM | provider={provider} | model={cfg['model']}")

        if provider == "openai":
            return ChatOpenAI(
                model_name   = cfg["model"],
                openai_api_key = cfg["api_key"],
                temperature  = cfg["temperature"],
                max_tokens   = cfg["max_tokens"],
                top_p        = cfg["top_p"],
                request_timeout = cfg["timeout"],
            )

        elif provider == "ollama":
            return Ollama(
                base_url    = cfg["base_url"],
                model       = cfg["model"],
                temperature = cfg["temperature"],
                num_predict = cfg["max_tokens"],
            )

        elif provider == "huggingface":
            from langchain_community.llms import HuggingFaceHub
            return HuggingFaceHub(
                repo_id        = cfg["model"],
                huggingfacehub_api_token = cfg["api_token"],
                task           = cfg["task"],
            )

        else:
            raise ValueError(f"Unknown LLM provider: {provider}")


# ============================================================
#  PROMPT TEMPLATES
# ============================================================

SYSTEM_PROMPT = AGENT_CONFIG["system_prompt"]

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("system",
     "Context retrieved from KLU documents and database:\n"
     "────────────────────────────────────────────────\n"
     "{context}\n"
     "────────────────────────────────────────────────\n"
     "Use ONLY the above context to answer. "
     "If the answer is not in the context, say: "
     "'I don't have verified information about that. "
     "Please contact the university office.'"),
    ("human", "{question}"),
])

CONVERSATIONAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{chat_history}\nUser: {question}"),
])


# ============================================================
#  RAG PIPELINE
# ============================================================

class RAGPipeline:
    """
    Core Retrieval-Augmented Generation pipeline.

    Architecture:
      1. Embed user query → dense vector
      2. Retrieve: Vector DB (ChromaDB + FAISS) + SQL DB
      3. Merge & rank context
      4. Generate answer with LLM (GPT/Llama/Mixtral)
      5. Return answer + citations + latency
    """

    def __init__(self):
        logger.info("🚀 Initialising RAG Pipeline...")
        self.embedder  = EmbeddingEngine()
        self.retriever = HybridRetriever()
        self.db        = UniversityDB()
        self.llm       = LLMFactory.build()
        self.memory    = ConversationBufferWindowMemory(
            k=AGENT_CONFIG["memory_window"],
            return_messages=True,
            memory_key="chat_history"
        )
        logger.info("✅ RAG Pipeline ready.")

    # ── Main Query Method ────────────────────────────────────
    def query(self, user_message: str, session_id: str = "default") -> Dict:
        t_start = time.time()
        logger.info(f"🔍 RAG Query | session={session_id} | msg='{user_message[:80]}'")

        # Step 1 — Embed query
        query_vec  = self.embedder.encode_query(user_message)

        # Step 2 — Retrieve from vector store
        doc_chunks = self.retriever.retrieve(
            query     = user_message,
            top_k     = 6,
            use_faiss = True,
            embedding = query_vec,
        )

        # Step 3 — Retrieve from SQL database (if structured query)
        db_context = self._fetch_db_context(user_message)

        # Step 4 — Merge and format context
        context = self._build_context(doc_chunks, db_context)

        # Step 5 — Generate answer via LLM
        messages = RAG_PROMPT.format_messages(
            context  = context,
            question = user_message,
        )
        response = self.llm.invoke(messages)
        answer   = response.content if hasattr(response, "content") else str(response)

        # Step 6 — Update memory
        self.memory.save_context(
            {"input" : user_message},
            {"output": answer}
        )

        latency = round((time.time() - t_start) * 1000, 1)
        logger.info(f"✅ Response generated in {latency}ms")

        return {
            "answer"    : answer,
            "sources"   : [c.get("metadata", {}).get("source", "KLU KB")
                           for c in doc_chunks],
            "chunks_used": len(doc_chunks),
            "db_context": bool(db_context),
            "latency_ms": latency,
            "model"     : LLM_CONFIG[LLM_CONFIG["active"]]["model"],
            "session_id": session_id,
        }

    # ── DB Context Helper ─────────────────────────────────────
    def _fetch_db_context(self, query: str) -> Optional[str]:
        """
        Attempts to fetch structured data from university DB
        if the query seems to be about student/course/schedule info.
        """
        q = query.lower()
        # Detect structured intent keywords
        if any(kw in q for kw in ["timetable", "schedule", "exam date", "fee",
                                   "attendance", "grade", "cgpa", "hostel room"]):
            logger.info("🗄️  Structured DB query detected — fetching from MySQL...")
            try:
                sample_sql = (
                    "SELECT course_code, course_name, credits, semester "
                    "FROM courses WHERE semester = 5 LIMIT 6;"
                )
                rows = self.db.execute_query(sample_sql)
                if rows:
                    return "Current semester courses: " + str(rows)
            except Exception as e:
                logger.warning(f"DB query failed (non-critical): {e}")
        return None

    # ── Context Builder ───────────────────────────────────────
    def _build_context(
        self,
        doc_chunks : List[Dict],
        db_context : Optional[str]
    ) -> str:
        parts = []
        for i, chunk in enumerate(doc_chunks, 1):
            src  = chunk.get("metadata", {}).get("source", "Document")
            text = chunk.get("text", "")
            parts.append(f"[Source {i} — {src}]\n{text}")

        if db_context:
            parts.append(f"[Source: University Database]\n{db_context}")

        return "\n\n".join(parts) if parts else "No relevant context found."

    def clear_memory(self, session_id: str = "default"):
        self.memory.clear()
        logger.info(f"🧹 Memory cleared for session: {session_id}")
