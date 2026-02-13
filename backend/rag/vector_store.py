"""
KLU Agent - Vector Store Module
Manages ChromaDB vector store for document storage and retrieval.
Handles document ingestion from JSON knowledge base and PDF files.
"""

import json
import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rag.embeddings import get_embedding_model
import config


_vector_store = None


def _flatten_json(data, prefix=""):
    """Recursively flatten nested JSON into text chunks with context."""
    documents = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix} > {key}" if prefix else key
            if isinstance(value, (dict, list)):
                documents.extend(_flatten_json(value, new_prefix))
            else:
                text = f"Topic: {new_prefix}\nInformation: {value}"
                documents.append(Document(
                    page_content=text,
                    metadata={"source": "klu_knowledge_base", "category": prefix.split(" > ")[0] if prefix else key}
                ))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                # For list of dicts, use 'name' field if available
                item_name = item.get("name", f"Item {i+1}")
                new_prefix = f"{prefix} > {item_name}"
                documents.extend(_flatten_json(item, new_prefix))
            else:
                text = f"Topic: {prefix}\nInformation: {item}"
                documents.append(Document(
                    page_content=text,
                    metadata={"source": "klu_knowledge_base", "category": prefix.split(" > ")[0] if prefix else "general"}
                ))

    return documents


def _create_structured_documents(data):
    """Create well-structured documents from KLU knowledge base for better retrieval."""
    documents = []

    # -- University Overview --
    if "university_overview" in data:
        overview = data["university_overview"]
        text = f"""KL University (KLU) Overview:
Full Name: {overview.get('full_name', '')}
Type: {overview.get('type', '')}
Established: {overview.get('established', '')}
Deemed University Status: {overview.get('deemed_status_year', '')}
Location: {overview.get('location', '')}
Campus Area: {overview.get('campus_area', '')}
Website: {overview.get('website', '')}
Accreditation: {', '.join(overview.get('accreditation', []))}
Rankings: {overview.get('rankings', '')}"""
        documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "overview"}))

    # -- Admissions --
    if "admissions" in data:
        admissions = data["admissions"]
        # B.Tech admissions
        if "undergraduate" in admissions and "btech" in admissions["undergraduate"]:
            btech = admissions["undergraduate"]["btech"]
            text = f"""B.Tech Admissions at KLU:
Eligibility: {btech.get('eligibility', '')}
Entrance Exams Accepted: {', '.join(btech.get('entrance_exams', []))}
Application Period: {btech.get('application_period', '')}
Application Fee: {btech.get('application_fee', '')}

Application Process:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(btech.get('process', [])))}

Documents Required:
{chr(10).join(f'- {doc}' for doc in btech.get('documents_required', []))}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "admissions"}))

        # MBA admissions
        if "postgraduate" in admissions and "mba" in admissions["postgraduate"]:
            mba = admissions["postgraduate"]["mba"]
            text = f"""MBA Admissions at KLU:
Eligibility: {mba.get('eligibility', '')}
Entrance Exams: {', '.join(mba.get('entrance_exams', []))}
Specializations: {', '.join(mba.get('specializations', []))}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "admissions"}))

        # PhD
        if "phd" in admissions:
            phd = admissions["phd"]
            text = f"""PhD Admissions at KLU:
Eligibility: {phd.get('eligibility', '')}
Entrance: {phd.get('entrance', '')}
Fellowship: {phd.get('fellowship', '')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "admissions"}))

    # -- Departments --
    if "departments" in data:
        for dept in data["departments"]:
            programs = ', '.join(dept.get('programs', []))
            specs = ', '.join(dept.get('specializations', []))
            labs = ', '.join(dept.get('labs', []))
            text = f"""Department: {dept['name']} ({dept['code']})
HOD: {dept.get('hod', 'N/A')}
Programs Offered: {programs}
Faculty Count: {dept.get('faculty_count', 'N/A')}
Specializations: {specs if specs else 'N/A'}
Laboratories: {labs if labs else 'N/A'}
Highlights: {dept.get('highlights', 'N/A')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "departments"}))

    # -- Placements --
    if "placements" in data:
        pl = data["placements"]
        stats = pl.get("statistics", {}).get("2023_24", {})
        text = f"""KLU Placement Statistics:
Overview: {pl.get('overview', '')}

2023-24 Statistics:
- Highest Package: {stats.get('highest_package_lpa', 'N/A')} LPA
- Average Package: {stats.get('average_package_lpa', 'N/A')} LPA
- Median Package: {stats.get('median_package_lpa', 'N/A')} LPA
- Placement Rate: {stats.get('placement_rate_percent', 'N/A')}%
- Companies Visited: {stats.get('companies_visited', 'N/A')}
- Total Offers: {stats.get('total_offers', 'N/A')}
- International Offers: {stats.get('international_offers', 'N/A')}

Top Recruiters: {', '.join(pl.get('top_recruiters', []))}

Training Programs:
{chr(10).join(f'- {t}' for t in pl.get('training_programs', []))}

Internship: {pl.get('internship_support', '')}"""
        documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "placements"}))

    # -- Campus Facilities --
    if "campus_facilities" in data:
        cf = data["campus_facilities"]

        # Library
        if "academic" in cf and "central_library" in cf["academic"]:
            lib = cf["academic"]["central_library"]
            text = f"""KLU Central Library:
Books: {lib.get('books', '')}
E-Resources: {lib.get('e_resources', '')}
Digital Library: {lib.get('digital_library', '')}
Seating Capacity: {lib.get('seating_capacity', '')}
Features: {', '.join(lib.get('features', []))}

Other Academic Facilities:
- Laboratories: {cf['academic'].get('laboratories', '')}
- Smart Classrooms: {cf['academic'].get('smart_classrooms', '')}
- Research Centers: {', '.join(cf['academic'].get('research_centers', []))}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "campus"}))

        # Sports
        if "sports" in cf:
            sports = cf["sports"]
            text = f"""KLU Sports Facilities:
Outdoor: {', '.join(sports.get('outdoor', []))}
Indoor: {', '.join(sports.get('indoor', []))}
Fitness: {', '.join(sports.get('fitness', []))}
Achievements: {sports.get('achievements', '')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "campus"}))

        # Other facilities
        if "other" in cf:
            other = cf["other"]
            text = f"""KLU Other Campus Facilities:
Medical: {other.get('medical', '')}
Transport: {other.get('transport', '')}
Canteens: {other.get('canteens', '')}
ATM: {other.get('atm', '')}
Auditorium: {other.get('auditorium', '')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "campus"}))

    # -- Fee Structure --
    if "fee_structure" in data:
        fees = data["fee_structure"]
        btech_fees = fees.get("btech", {}).get("general", {})
        hostel = fees.get("hostel_fees", {})
        scholarships = fees.get("scholarships", {})
        text = f"""KLU Fee Structure:

B.Tech (General):
- Tuition Fee: ₹{btech_fees.get('tuition_fee_per_year', 'N/A')}/year
- Other Fees: ₹{btech_fees.get('other_fees_per_year', 'N/A')}/year
- Total: ₹{btech_fees.get('total_per_year', 'N/A')}/year

Hostel Fees:
- Single AC: ₹{hostel.get('single_ac_per_year', 'N/A')}/year
- Double Sharing AC: ₹{hostel.get('double_sharing_ac_per_year', 'N/A')}/year
- Triple Sharing Non-AC: ₹{hostel.get('triple_sharing_non_ac_per_year', 'N/A')}/year
- Mess Charges: ₹{hostel.get('mess_charges_per_year', 'N/A')}/year

Transport: ₹{fees.get('transport_fee_per_year', 'N/A')}

Scholarships:
- Merit Based: {scholarships.get('merit_based', '')}
- Sports Quota: {scholarships.get('sports_quota', '')}
- Need Based: {scholarships.get('need_based', '')}
- Research Fellowship: {scholarships.get('research_fellowship', '')}

Payment Options: {', '.join(fees.get('payment_options', []))}"""
        documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "fees"}))

    # -- Academic Calendar --
    if "academic_calendar" in data:
        cal = data["academic_calendar"]
        odd = cal.get("odd_semester", {})
        even = cal.get("even_semester", {})
        events_cal = cal.get("important_events", {})
        text = f"""KLU Academic Calendar:

Odd Semester (July - December):
- Classes Begin: {odd.get('classes_begin', '')}
- Mid-Sem Exams: {odd.get('mid_semester_exams', '')}
- End-Sem Exams: {odd.get('end_semester_exams', '')}
- Winter Break: {odd.get('winter_break', '')}

Even Semester (January - June):
- Classes Begin: {even.get('classes_begin', '')}
- Mid-Sem Exams: {even.get('mid_semester_exams', '')}
- End-Sem Exams: {even.get('end_semester_exams', '')}
- Summer Break: {even.get('summer_break', '')}

Important Events:
- Foundation Day: {events_cal.get('foundation_day', '')}
- SAMYAK Tech Fest: {events_cal.get('samyak_tech_fest', '')}
- Cultural Fest: {events_cal.get('cultural_fest', '')}
- Convocation: {events_cal.get('convocation', '')}"""
        documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "schedule"}))

    # -- Student Clubs --
    if "student_clubs" in data:
        clubs_text = "Student Clubs at KLU:\n\n"
        for club in data["student_clubs"]:
            clubs_text += f"• {club['name']}: {club.get('focus', '')}. Activities: {club.get('activities', '')}\n"
        documents.append(Document(page_content=clubs_text, metadata={"source": "klu_knowledge_base", "category": "clubs"}))

    # -- Events & Fests --
    if "events_and_fests" in data:
        ef = data["events_and_fests"]
        if "samyak" in ef:
            s = ef["samyak"]
            text = f"""SAMYAK - KLU Annual Tech Fest:
Type: {s.get('type', '')}
Description: {s.get('description', '')}
When: {s.get('typical_month', '')}
Activities: {', '.join(s.get('activities', []))}
Expected Footfall: {s.get('footfall', '')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "events"}))

        if "surabhi" in ef:
            su = ef["surabhi"]
            text = f"""SURABHI - KLU Annual Cultural Fest:
Type: {su.get('type', '')}
Description: {su.get('description', '')}
When: {su.get('typical_month', '')}
Activities: {', '.join(su.get('activities', []))}
Expected Footfall: {su.get('footfall', '')}"""
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "events"}))

        if "regular_events" in ef:
            text = "Regular Events at KLU:\n" + "\n".join(f"- {e}" for e in ef["regular_events"])
            documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "events"}))

    # -- Contact Information --
    if "contact_information" in data:
        ci = data["contact_information"]
        text = f"""KLU Contact Information:
Address: {ci.get('address', '')}

Admissions Office: {ci.get('admissions_office', {}).get('email', '')} | {ci.get('admissions_office', {}).get('phone', '')} | Timing: {ci.get('admissions_office', {}).get('timing', '')}
Placement Cell: {ci.get('placement_cell', {}).get('email', '')}
Hostel Office: {ci.get('hostel_office', {}).get('email', '')}
Examination Cell: {ci.get('examination_cell', {}).get('email', '')}
General Enquiry: {ci.get('general_enquiry', {}).get('email', '')} | {ci.get('general_enquiry', {}).get('phone', '')}"""
        documents.append(Document(page_content=text, metadata={"source": "klu_knowledge_base", "category": "contact"}))

    return documents


def load_knowledge_base():
    """Load KLU knowledge base JSON and create document chunks."""
    kb_path = Path(config.BASE_DIR) / "knowledge_base" / "klu_data.json"

    if not kb_path.exists():
        print(f"⚠️ Knowledge base not found at {kb_path}")
        return []

    with open(kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create structured documents
    documents = _create_structured_documents(data)

    # Also add flattened versions for broader coverage
    flat_docs = _flatten_json(data)
    documents.extend(flat_docs)

    print(f"📄 Loaded {len(documents)} documents from knowledge base")
    return documents


def load_pdf_documents():
    """Load PDF documents from the documents directory."""
    docs_dir = Path(config.DOCUMENTS_DIR)

    if not docs_dir.exists():
        os.makedirs(docs_dir, exist_ok=True)
        print(f"📁 Created documents directory at {docs_dir}")
        return []

    documents = []
    try:
        from langchain_community.document_loaders import PyPDFLoader

        for pdf_file in docs_dir.glob("*.pdf"):
            print(f"📄 Loading PDF: {pdf_file.name}")
            loader = PyPDFLoader(str(pdf_file))
            documents.extend(loader.load())
    except ImportError:
        print("⚠️ PyPDF not available, skipping PDF loading")

    print(f"📄 Loaded {len(documents)} pages from PDFs")
    return documents


def initialize_vector_store():
    """Initialize ChromaDB vector store with all documents."""
    global _vector_store

    print("🔄 Initializing vector store...")

    # Load all documents
    all_documents = []
    all_documents.extend(load_knowledge_base())
    all_documents.extend(load_pdf_documents())

    if not all_documents:
        print("⚠️ No documents found to index!")
        return None

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"🔪 Split into {len(chunks)} chunks")

    # Get embedding model
    embedding_model = get_embedding_model()

    # Create ChromaDB vector store
    _vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=config.CHROMA_PERSIST_DIR,
        collection_name=config.CHROMA_COLLECTION_NAME
    )

    print(f"✅ Vector store initialized with {len(chunks)} chunks")
    return _vector_store


def get_vector_store():
    """Get the vector store, initializing if needed."""
    global _vector_store

    if _vector_store is None:
        # Try loading existing store first
        if os.path.exists(config.CHROMA_PERSIST_DIR):
            try:
                embedding_model = get_embedding_model()
                _vector_store = Chroma(
                    persist_directory=config.CHROMA_PERSIST_DIR,
                    embedding_function=embedding_model,
                    collection_name=config.CHROMA_COLLECTION_NAME
                )
                # Check if it has documents
                if _vector_store._collection.count() > 0:
                    print(f"✅ Loaded existing vector store with {_vector_store._collection.count()} documents")
                    return _vector_store
            except Exception as e:
                print(f"⚠️ Failed to load existing vector store: {e}")

        # Initialize fresh
        _vector_store = initialize_vector_store()

    return _vector_store


def get_retriever():
    """Get a retriever from the vector store."""
    store = get_vector_store()
    if store is None:
        return None

    return store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": config.TOP_K_RESULTS,
            "fetch_k": config.TOP_K_RESULTS * 3
        }
    )
