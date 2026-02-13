"""
KLU Agent - Agentic Framework Module
Implements the LangChain Agent with tools for:
1. RAG-based document retrieval
2. SQL database querying
3. FAQ lookup
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from sqlalchemy import text as sql_text
from data.database import SessionLocal, Course, Department, Event, HostelInfo, FAQ
from rag.vector_store import get_retriever
from rag.chain import get_llm
import config


# ============================================
# Agent Tools
# ============================================

def search_knowledge_base(query: str) -> str:
    """Search the KLU knowledge base using RAG for relevant information."""
    retriever = get_retriever()
    if retriever is None:
        return "Knowledge base is not available."

    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the knowledge base."

    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("category", "general")
        results.append(f"[Source: {source}]\n{doc.page_content}")

    return "\n\n---\n\n".join(results)


def query_courses(query: str) -> str:
    """Query the database for course information. Input should be a search term like department name, course level (UG/PG), or course name."""
    session = SessionLocal()
    try:
        search_term = f"%{query}%"
        courses = session.query(Course).join(Department).filter(
            (Course.name.ilike(search_term)) |
            (Department.name.ilike(search_term)) |
            (Department.code.ilike(search_term)) |
            (Course.level.ilike(search_term))
        ).all()

        if not courses:
            return f"No courses found matching '{query}'."

        results = []
        for c in courses:
            dept = session.query(Department).filter_by(id=c.department_id).first()
            dept_name = dept.name if dept else "N/A"
            results.append(
                f"• {c.name} ({c.code})\n"
                f"  Department: {dept_name}\n"
                f"  Level: {c.level} | Duration: {c.duration_years} years\n"
                f"  Seats: {c.total_seats} | Fee: ₹{c.fee_per_year:,.0f}/year"
            )

        return f"Found {len(courses)} course(s):\n\n" + "\n\n".join(results)
    finally:
        session.close()


def query_events(query: str) -> str:
    """Query upcoming events at KLU. Input can be event type (tech/workshop/seminar/cultural) or general search term."""
    session = SessionLocal()
    try:
        search_term = f"%{query}%"
        events = session.query(Event).filter(
            (Event.name.ilike(search_term)) |
            (Event.event_type.ilike(search_term)) |
            (Event.description.ilike(search_term))
        ).filter(Event.is_upcoming == True).all()

        if not events:
            return f"No upcoming events found matching '{query}'."

        results = []
        for e in events:
            results.append(
                f"📅 {e.name}\n"
                f"   Type: {e.event_type} | Date: {e.date}\n"
                f"   Venue: {e.venue}\n"
                f"   {e.description}"
            )

        return f"Found {len(events)} upcoming event(s):\n\n" + "\n\n".join(results)
    finally:
        session.close()


def query_hostel(query: str) -> str:
    """Query hostel information. Input can be hostel type (boys/girls), room type, or general search."""
    session = SessionLocal()
    try:
        search_term = f"%{query}%"
        hostels = session.query(HostelInfo).filter(
            (HostelInfo.hostel_name.ilike(search_term)) |
            (HostelInfo.hostel_type.ilike(search_term)) |
            (HostelInfo.room_type.ilike(search_term))
        ).all()

        if not hostels:
            return f"No hostel information found matching '{query}'."

        results = []
        for h in hostels:
            results.append(
                f"🏠 {h.hostel_name}\n"
                f"   Type: {h.hostel_type} | Room: {h.room_type}\n"
                f"   Fee: ₹{h.fee_per_year:,.0f}/year | Capacity: {h.capacity}\n"
                f"   Amenities: {h.amenities}"
            )

        return f"Found {len(hostels)} hostel option(s):\n\n" + "\n\n".join(results)
    finally:
        session.close()


def query_faqs(query: str) -> str:
    """Search frequently asked questions. Input should be keywords from the question."""
    session = SessionLocal()
    try:
        search_term = f"%{query}%"
        faqs = session.query(FAQ).filter(
            (FAQ.question.ilike(search_term)) |
            (FAQ.answer.ilike(search_term)) |
            (FAQ.category.ilike(search_term))
        ).limit(5).all()

        if not faqs:
            return f"No FAQs found matching '{query}'."

        results = []
        for f in faqs:
            results.append(f"Q: {f.question}\nA: {f.answer}")

        return "\n\n".join(results)
    finally:
        session.close()


def query_departments(query: str) -> str:
    """Query department information from the database. Input should be department name or code."""
    session = SessionLocal()
    try:
        search_term = f"%{query}%"
        depts = session.query(Department).filter(
            (Department.name.ilike(search_term)) |
            (Department.code.ilike(search_term))
        ).all()

        if not depts:
            return f"No departments found matching '{query}'."

        results = []
        for d in depts:
            course_count = session.query(Course).filter_by(department_id=d.id).count()
            results.append(
                f"🏛️ {d.name} ({d.code})\n"
                f"   HOD: {d.hod}\n"
                f"   Faculty: {d.faculty_count} | Courses: {course_count}\n"
                f"   {d.description}"
            )

        return f"Found {len(depts)} department(s):\n\n" + "\n\n".join(results)
    finally:
        session.close()


# ============================================
# Define Agent Tools
# ============================================

AGENT_TOOLS = [
    Tool(
        name="SearchKnowledgeBase",
        func=search_knowledge_base,
        description="Search the KLU knowledge base for general information about admissions, fees, placements, campus facilities, academic calendar, student clubs, events, and university overview. Use this for broad or general questions."
    ),
    Tool(
        name="QueryCourses",
        func=query_courses,
        description="Query the database for specific course information including course names, departments, fees, seats, and duration. Use when user asks about specific courses or programs."
    ),
    Tool(
        name="QueryEvents",
        func=query_events,
        description="Query upcoming events, workshops, seminars, and fests at KLU. Use when user asks about events or activities."
    ),
    Tool(
        name="QueryHostel",
        func=query_hostel,
        description="Query hostel details including room types, fees, amenities, and capacity. Use when user asks about accommodation."
    ),
    Tool(
        name="QueryFAQs",
        func=query_faqs,
        description="Search frequently asked questions about KLU. Use when the question seems like a common query."
    ),
    Tool(
        name="QueryDepartments",
        func=query_departments,
        description="Query department information including HOD, faculty count, and description. Use when user asks about specific departments."
    )
]


# ============================================
# Agent Prompt
# ============================================

AGENT_PROMPT = PromptTemplate.from_template("""You are **KLU Agent**, the official AI assistant for KL University (KLU), Vaddeswaram, Andhra Pradesh, India.

You have access to the following tools to answer questions accurately:

{tools}

## Instructions:
1. Use the tools to find accurate information before answering.
2. ALWAYS use at least one tool before giving your final answer.
3. NEVER make up information. If tools return no results, say you don't have that information.
4. Be friendly, professional, and use markdown formatting.
5. When providing fees, always include ₹ symbol.
6. For complex questions, use multiple tools if needed.

Use the following format:

Question: the input question you must answer
Thought: think about what tool(s) to use
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question (use markdown formatting)

Begin!

Question: {input}
Thought: {agent_scratchpad}""")


# ============================================
# Agent Builder
# ============================================

def create_klu_agent():
    """Create and return the KLU Agent with all tools."""
    llm = get_llm()

    agent = create_react_agent(
        llm=llm,
        tools=AGENT_TOOLS,
        prompt=AGENT_PROMPT
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=AGENT_TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        return_intermediate_steps=True
    )

    return agent_executor


def run_agent(query: str) -> dict:
    """
    Run the KLU Agent on a query and return structured response.

    Returns:
        dict with 'answer', 'sources', and 'tools_used'
    """
    agent = create_klu_agent()

    try:
        result = agent.invoke({"input": query})

        # Extract tools used from intermediate steps
        tools_used = []
        sources = set()
        for step in result.get("intermediate_steps", []):
            if len(step) >= 2:
                action = step[0]
                tools_used.append(action.tool)
                # Add source based on tool
                if action.tool == "SearchKnowledgeBase":
                    sources.add("KLU Knowledge Base (Documents)")
                elif action.tool in ["QueryCourses", "QueryEvents", "QueryHostel", "QueryFAQs", "QueryDepartments"]:
                    sources.add("KLU College Database")

        return {
            "answer": result.get("output", "I couldn't generate a response. Please try again."),
            "sources": list(sources) if sources else ["KLU Knowledge Base"],
            "tools_used": tools_used
        }

    except Exception as e:
        print(f"❌ Agent error: {e}")
        # Fallback to simple RAG if agent fails
        return _fallback_rag(query)


def _fallback_rag(query: str) -> dict:
    """Fallback to simple RAG if agent fails."""
    try:
        from rag.chain import build_rag_chain
        retriever = get_retriever()
        if retriever is None:
            return {
                "answer": "I'm having trouble accessing my knowledge base. Please try again later.",
                "sources": [],
                "tools_used": ["fallback"]
            }

        chain = build_rag_chain(retriever)
        result = chain.invoke({"question": query, "db_context": "No database results available."})

        return {
            "answer": result,
            "sources": ["KLU Knowledge Base (Fallback)"],
            "tools_used": ["RAG-fallback"]
        }
    except Exception as e:
        return {
            "answer": f"I apologize, but I'm experiencing technical difficulties. Please contact the KLU office directly for assistance. Error: {str(e)}",
            "sources": [],
            "tools_used": ["error"]
        }
