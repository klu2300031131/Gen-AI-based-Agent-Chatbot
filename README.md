# 🎓 Gen-AI Based Agent Chatbot — KLU Smart Assistant

> An Agentic RAG (Retrieval-Augmented Generation) chatbot for **KL University**, built using LangChain, ChromaDB, FAISS, HuggingFace Transformers, and a fine-tuned DistilBERT intent classifier.

---

## 🚀 Features

- 🤖 **Agentic Framework** — LangChain ReAct Agent with multiple tools
- 📚 **RAG Pipeline** — ChromaDB + FAISS hybrid retrieval over KLU documents
- 🗄️ **College Database Integration** — MySQL via SQLAlchemy ORM
- 🧠 **NLP Intent Classification** — TF-IDF + Naive Bayes + DistilBERT fine-tuned
- 💬 **Conversational Memory** — Multi-turn chat with context window
- 🌐 **Web Interface** — Clean, responsive HTML/CSS/JS frontend
- ⚡ **Offline Mode** — Full chatbot works without internet using local knowledge base

---

## 🏗️ Architecture

```
User Query
    │
    ▼
[LangChain ReAct Agent]
    │
    ├──► KnowledgeBaseTool  → Local JSON KB (admissions, fees, hostel, mess...)
    ├──► RAGDocumentTool    → ChromaDB + FAISS (PDF/TXT documents)
    ├──► DatabaseQueryTool  → MySQL (timetable, results, fee status)
    └──► GpaCalculatorTool  → Computes SGPA/CGPA
    │
    ▼
[LLM: GPT-4o / Llama 3.1 / Mixtral-8x7B]
    │
    ▼
Structured, Verified Response
```

---

## 📁 Project Structure

```
Gen-AI-based-Agent-Catbott/
│
├── 🌐 Frontend (Offline Chatbot)
│   ├── index.html              # Main chat UI
│   ├── style.css               # University theme design
│   ├── script.js               # Chatbot engine (keyword matching)
│   ├── knowledgeBase.js        # Embedded JS knowledge base
│   └── knowledgeBase.json      # Full KLU knowledge base (JSON)
│
├── 🤖 Agentic RAG Backend
│   ├── agent.py                # LangChain ReAct Agent + Tools
│   ├── rag_pipeline.py         # RAG: Embed → Retrieve → Generate
│   ├── vector_store.py         # ChromaDB + FAISS hybrid retriever
│   ├── embeddings.py           # HuggingFace sentence-transformers
│   ├── database.py             # MySQL ORM (Students, Faculty, Courses)
│   ├── server.py               # Flask REST API + training pipeline
│   └── config.py               # Centralised configuration
│
├── 📄 docs/                    # Documents for RAG ingestion
│   ├── klu_academic_handbook.txt
│   └── klu_placement_policy.txt
│
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variables template
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangChain ReAct |
| Vector DB | ChromaDB + FAISS |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM Options | GPT-4o / Llama 3.1 (Ollama) / Mixtral-8x7B |
| Intent Classifier | DistilBERT (fine-tuned) + TF-IDF Naive Bayes |
| Database | MySQL + SQLAlchemy ORM |
| Backend | Python Flask / FastAPI |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

---

## 🔧 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/klu2300031131/Gen-AI-based-Agent-Catbott.git
cd Gen-AI-based-Agent-Catbott
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
copy .env.example .env       # Windows
cp .env.example .env         # Linux/Mac
# Edit .env with your API keys and DB credentials
```

### 5. Run the backend server
```bash
python server.py
```

### 6. Open the chatbot
Simply open `index.html` in your browser — it works fully offline!

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Server health check |
| POST | `/api/chat` | Send message, get AI response |
| GET | `/api/train/status` | Model training status & metrics |
| GET | `/api/kb/stats` | Knowledge base statistics |
| GET | `/api/kb/intents` | All intent class mappings |

---

## 🎯 Knowledge Base Coverage

| Topic | Details |
|---|---|
| 🎓 Admissions | Eligibility, steps, deadlines, counselling, reservations |
| 📚 Courses | 5 schools, 20+ UG/PG programs, credit system |
| 💼 Placements | Year-wise 2021–2025, 15+ recruiters, packages |
| 🏠 Hostel | 8,000 capacity, room types, rules, security |
| 🍛 Mess Food | Full 7-day menu with all meals |
| 💰 Fees | All programs, scholarships, installments |
| 🎉 Events | Samyak, Surabhi, E-Summit, hackathons |
| 📅 Academic Calendar | Semester dates, exams, holidays |

---

## 👨‍💻 Author

**Student ID:** 2300031131  
**University:** KL University, Vaddeswaram, Andhra Pradesh  
**Course:** B.Tech CSE  

---

## 📜 License

This project is for academic purposes at KL University.
