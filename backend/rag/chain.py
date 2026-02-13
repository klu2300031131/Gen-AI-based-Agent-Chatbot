"""
KLU Agent - RAG Chain Module
Builds the LangChain RAG chain for context-grounded responses.
"""

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import config


# System prompt that grounds the AI in institutional data
RAG_SYSTEM_PROMPT = """You are **KLU Agent**, the official AI assistant for KL University (Koneru Lakshmaiah Education Foundation), located in Vaddeswaram, Guntur District, Andhra Pradesh, India.

## Your Role:
- Provide accurate, helpful, and friendly responses about KLU
- Answer questions about admissions, courses, departments, placements, campus facilities, fees, events, hostel, schedules, and student life
- You MUST base your answers ONLY on the provided context from the knowledge base and database
- If the answer is not found in the context, clearly say: "I don't have specific information about that in my knowledge base. Please contact the relevant KLU office for accurate details."

## Rules:
1. NEVER fabricate or hallucinate information. Only use facts from the provided context.
2. Be conversational, warm, and professional.
3. Use markdown formatting for readability (headers, bullet points, bold text, tables).
4. When mentioning fees, always mention the currency (₹ or INR).
5. If a question is ambiguous, ask for clarification.
6. For urgent or sensitive matters, direct students to the appropriate office.
7. Include relevant source information when possible.
8. Keep responses concise but comprehensive.

## Context from Knowledge Base:
{context}

## Database Query Results (if available):
{db_context}
"""

RAG_USER_PROMPT = """Student/User Question: {question}

Please provide a helpful, accurate response based on the context above. If the context doesn't contain enough information, say so clearly."""


def get_llm():
    """Get the configured LLM."""
    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=config.TEMPERATURE,
            convert_system_message_to_human=True
        )
    elif config.LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
            temperature=config.TEMPERATURE
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")


def build_rag_chain(retriever):
    """
    Build a RAG chain that retrieves relevant context and generates a grounded response.
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", RAG_USER_PROMPT)
    ])

    def format_docs(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "db_context": lambda x: x.get("db_context", "No database results."),
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
