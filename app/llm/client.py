import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

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
