# ============================================================
#  KLU Smart Assistant — Agentic Framework
#  LangChain ReAct Agent with Custom Tools
#
#  The Agent decides WHICH tool to call based on the query:
#    • RAGDocumentTool    — search KLU PDF/text documents
#    • DatabaseQueryTool  — query structured university DB
#    • KnowledgeBaseTool  — search local JSON knowledge base
#    • CalculatorTool     — compute GPA, fees, etc.
#    • WeatherTool        — campus weather (dummy)
#
#  Architecture: ReAct (Reason + Act) loop
#  Framework   : LangChain AgentExecutor
# ============================================================

import json
import logging
import datetime
from typing import Optional, Any

from langchain.agents           import AgentExecutor, create_react_agent
from langchain.tools            import BaseTool, tool
from langchain.memory           import ConversationBufferWindowMemory
from langchain.callbacks        import StdOutCallbackHandler
from langchain_core.prompts     import PromptTemplate
from langchain_core.messages    import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from config       import AGENT_CONFIG, LLM_CONFIG
from rag_pipeline import RAGPipeline, LLMFactory
from database     import UniversityDB

logger = logging.getLogger("KLU.Agent")


# ============================================================
#  TOOL INPUT SCHEMAS
# ============================================================

class DocumentSearchInput(BaseModel):
    query: str = Field(..., description="The question to search in KLU documents")

class DatabaseQueryInput(BaseModel):
    query: str = Field(..., description="Natural language query to run against university DB")
    table: Optional[str] = Field(None, description="Specific table: students/faculty/courses/timetable")

class KBSearchInput(BaseModel):
    query   : str = Field(..., description="The topic to search in KLU knowledge base")
    section : Optional[str] = Field(None, description="Section: admissions/placements/hostel/fees/mess")

class GpaCalculatorInput(BaseModel):
    grades  : str = Field(..., description="Comma-separated list of grades, e.g. 'A+,A,B+,B,A'")
    credits : str = Field(..., description="Comma-separated credits matching each grade, e.g. '4,3,4,3,3'")


# ============================================================
#  TOOLS
# ============================================================

class RAGDocumentTool(BaseTool):
    """Searches through KLU official documents (PDFs, handbooks, circulars)."""

    name        : str = "klu_document_search"
    description : str = (
        "Search through KLU official documents including academic handbooks, "
        "circulars, policy documents, syllabi, and research papers. "
        "Use this when the user asks about official policies, syllabus, "
        "academic rules, or anything from documents."
    )
    args_schema : type[BaseModel] = DocumentSearchInput

    rag: Any = None     # injected at runtime

    def _run(self, query: str) -> str:
        logger.info(f"🔧 [Tool] RAGDocumentTool called | query='{query[:60]}'")
        try:
            result = self.rag.query(query)
            return f"Document search result:\n{result['answer']}\n(Sources: {result['sources']})"
        except Exception as e:
            logger.error(f"RAGDocumentTool error: {e}")
            return f"Could not retrieve document information: {str(e)}"

    async def _arun(self, query: str) -> str:
        return self._run(query)


class DatabaseQueryTool(BaseTool):
    """Queries structured university database for real-time information."""

    name        : str = "klu_database_query"
    description : str = (
        "Query the KLU university database for structured, real-time data like: "
        "student records, faculty details, course list, timetable, exam schedule, "
        "fee payment status, hostel room allocation, and attendance. "
        "Use this when asking for specific or personalised student/course information."
    )
    args_schema : type[BaseModel] = DatabaseQueryInput

    db: Any = None

    def _run(self, query: str, table: Optional[str] = None) -> str:
        logger.info(f"🔧 [Tool] DatabaseQueryTool called | query='{query[:60]}'")
        try:
            q = query.lower()
            if "timetable" in q or "schedule" in q:
                result = self.db.get_timetable(branch="CSE", year=2, day="Monday")
                return f"Timetable data: {json.dumps(result, indent=2)}"
            elif "course" in q:
                result = self.db.execute_query(
                    "SELECT course_code, course_name, credits FROM courses LIMIT 10;"
                )
                return f"Available courses: {json.dumps(result, indent=2)}"
            elif "faculty" in q:
                result = self.db.get_faculty_by_dept("Computer Science")
                return f"Faculty details: {json.dumps(result, indent=2)}"
            elif "fee" in q:
                return ("Fee information: Tuition fee for B.Tech CSE is ₹1,65,000/year. "
                        "Please contact the finance office with your roll number.")
            else:
                return (f"Database query received for: '{query}'. "
                        f"Please provide a specific roll number or course code.")
        except Exception as e:
            logger.error(f"DatabaseQueryTool error: {e}")
            return f"Database lookup failed: {str(e)}"

    async def _arun(self, query: str, table: Optional[str] = None) -> str:
        return self._run(query, table)


class KnowledgeBaseTool(BaseTool):
    """Searches the local KLU knowledge base for university information."""

    name        : str = "klu_knowledge_base"
    description : str = (
        "Search the KLU Smart Assistant knowledge base for general university information: "
        "admissions, placements, hostel, mess menu, fees, events, faculty stats, "
        "campus infrastructure, academic calendar, student clubs, etc. "
        "Use this as the FIRST tool for most general university queries."
    )
    args_schema : type[BaseModel] = KBSearchInput

    kb_path: str = "knowledgeBase.json"

    def _run(self, query: str, section: Optional[str] = None) -> str:
        logger.info(f"🔧 [Tool] KnowledgeBaseTool called | query='{query[:60]}' | section={section}")
        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                kb = json.load(f)

            # Filter to section if provided
            if section and section in kb:
                data = kb[section]
            else:
                # Keyword-based section routing
                q = query.lower()
                if   any(k in q for k in ["admission", "eligibility", "apply"]): data = kb.get("admissions", {})
                elif any(k in q for k in ["placement", "salary", "package"])    : data = kb.get("placements", {})
                elif any(k in q for k in ["hostel", "room", "accommodation"])   : data = kb.get("hostel", {})
                elif any(k in q for k in ["mess", "food", "menu"])              : data = kb.get("mess_food", {})
                elif any(k in q for k in ["fee", "scholarship", "payment"])     : data = kb.get("fees", {})
                elif any(k in q for k in ["event", "fest", "samyak", "surabhi"]): data = kb.get("events", {})
                elif any(k in q for k in ["faculty", "teacher", "professor"])   : data = kb.get("faculty", {})
                elif any(k in q for k in ["campus", "library", "lab", "sport"]) : data = kb.get("infrastructure", {})
                elif any(k in q for k in ["exam", "semester", "holiday"])       : data = kb.get("academic_calendar", {})
                else:                                                              data = kb.get("university", {})

            summary = json.dumps(data, indent=2)[:1500]  # truncate for context window
            return f"Knowledge Base result for '{query}':\n{summary}"
        except Exception as e:
            logger.error(f"KnowledgeBaseTool error: {e}")
            return f"Knowledge base lookup failed: {str(e)}"

    async def _arun(self, query: str, section: Optional[str] = None) -> str:
        return self._run(query, section)


class GpaCalculatorTool(BaseTool):
    """Computes CGPA/SGPA from grades and credits."""

    name        : str = "gpa_calculator"
    description : str = (
        "Calculate SGPA or CGPA given a list of grades and corresponding credits. "
        "Use this when a student wants to calculate their GPA. "
        "Input format: grades='A+,A,B+' credits='4,3,4'"
    )
    args_schema : type[BaseModel] = GpaCalculatorInput

    GRADE_POINTS = {
        "O": 10, "A+": 9, "A": 8, "B+": 7,
        "B": 6,  "C": 5,  "D": 4, "F": 0
    }

    def _run(self, grades: str, credits: str) -> str:
        logger.info(f"🔧 [Tool] GpaCalculatorTool called | grades={grades} | credits={credits}")
        try:
            g_list = [g.strip().upper() for g in grades.split(",")]
            c_list = [int(c.strip())    for c in credits.split(",")]

            if len(g_list) != len(c_list):
                return "Error: Number of grades and credits must match."

            weighted_sum  = sum(self.GRADE_POINTS.get(g, 0) * c
                                for g, c in zip(g_list, c_list))
            total_credits = sum(c_list)
            gpa           = round(weighted_sum / total_credits, 2) if total_credits else 0

            breakdown = "\n".join(
                f"  {g:3s} × {c:2d} credits = {self.GRADE_POINTS.get(g, 0) * c} points"
                for g, c in zip(g_list, c_list)
            )

            return (
                f"📊 GPA Calculation Result:\n"
                f"{breakdown}\n"
                f"─────────────────────────\n"
                f"Total Credits : {total_credits}\n"
                f"Total Points  : {weighted_sum}\n"
                f"SGPA          : {gpa} / 10.0\n"
                f"\n(Grade scale: O=10, A+=9, A=8, B+=7, B=6, C=5, D=4, F=0)"
            )
        except Exception as e:
            return f"GPA calculation failed: {str(e)}"

    async def _arun(self, grades: str, credits: str) -> str:
        return self._run(grades, credits)


# ============================================================
#  REACT AGENT PROMPT
# ============================================================

REACT_PROMPT_TEMPLATE = """You are KLU Smart Assistant, an expert AI agent for KL University.
You have access to the following tools:

{tools}

Use the following format to answer:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat up to {max_iterations} times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important rules:
- Always prefer KnowledgeBaseTool for general KLU questions
- Use DatabaseQueryTool only for specific student/course/fee data
- Use RAGDocumentTool for policy/syllabus questions
- Always cite your source in the final answer
- Never make up information — say you don't know if uncertain

Previous conversation:
{chat_history}

Question: {input}
{agent_scratchpad}"""


# ============================================================
#  AGENT BUILDER
# ============================================================

class KLUAgentBuilder:
    """
    Builds and returns a LangChain ReAct AgentExecutor
    with all KLU tools wired in.
    """

    def __init__(self):
        logger.info("🏗️  Building KLU ReAct Agent...")
        self.rag = RAGPipeline()
        self.db  = UniversityDB()
        self.llm = LLMFactory.build()

        self.tools = self._build_tools()
        self.memory = ConversationBufferWindowMemory(
            k=AGENT_CONFIG["memory_window"],
            return_messages=True,
            memory_key="chat_history",
            input_key="input",
        )
        self.agent_executor = self._build_agent()
        logger.info("✅ KLU ReAct Agent ready.")

    def _build_tools(self):
        doc_tool   = RAGDocumentTool(rag=self.rag)
        db_tool    = DatabaseQueryTool(db=self.db)
        kb_tool    = KnowledgeBaseTool()
        gpa_tool   = GpaCalculatorTool()
        return [kb_tool, db_tool, doc_tool, gpa_tool]

    def _build_agent(self):
        prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE).partial(
            max_iterations=AGENT_CONFIG["max_iterations"]
        )
        agent = create_react_agent(
            llm   = self.llm,
            tools = self.tools,
            prompt = prompt,
        )
        return AgentExecutor(
            agent              = agent,
            tools              = self.tools,
            memory             = self.memory,
            max_iterations     = AGENT_CONFIG["max_iterations"],
            max_execution_time = AGENT_CONFIG["max_exec_time"],
            verbose            = AGENT_CONFIG["verbose"],
            handle_parsing_errors = AGENT_CONFIG["handle_errors"],
            callbacks          = [StdOutCallbackHandler()],
            return_intermediate_steps = True,
        )

    def chat(self, user_message: str, session_id: str = "default") -> dict:
        """Main entry point for agent-driven chat."""
        logger.info(f"🤖 Agent invoked | session={session_id} | msg='{user_message[:80]}'")
        result = self.agent_executor.invoke({
            "input": user_message,
            "chat_history": self.memory.load_memory_variables({}).get("chat_history", [])
        })

        steps = result.get("intermediate_steps", [])
        tools_used = [step[0].tool for step in steps]

        return {
            "answer"     : result.get("output", ""),
            "tools_used" : tools_used,
            "steps"      : len(steps),
            "session_id" : session_id,
            "timestamp"  : datetime.datetime.now().isoformat(),
        }


# ============================================================
#  QUICK TEST
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("🧪 Running agent self-test...")

    agent = KLUAgentBuilder()
    test_queries = [
        "What are the placement statistics for 2025?",
        "Tell me about the hostel facilities at KLU",
        "Calculate my SGPA: grades A+,A,B+,A credits 4,3,4,3",
        "What is the mess menu for Sunday?",
    ]
    for q in test_queries:
        print(f"\n{'='*60}\nQ: {q}")
        res = agent.chat(q)
        print(f"A: {res['answer'][:300]}")
        print(f"Tools used: {res['tools_used']}")
