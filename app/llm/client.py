# app/llm/client.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

def get_llm() -> ChatGroq:
    """
    Returns a configured Groq LLM client.
    Model: openai/gpt-oss-120b
    Temperature 0 = deterministic (same input -> same output).
    Good for code generation where we want consistency.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment. Check your .env file.")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key
    )


def call_llm(prompt: str) -> str:
    """
    Send a prompt string to the LLM, return the response as a plain string.
    This is the single function all nodes will use to talk to the LLM.
    """
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
