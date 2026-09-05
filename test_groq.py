"""
Phase 1 test: Verify Groq API is working.
Run this with: python test_groq.py
"""
from app.llm.client import get_llm
from langchain_core.messages import HumanMessage

def test_groq_connection():
    print("Testing Groq API connection...")
    
    llm = get_llm()
    
    # Simple test message
    response = llm.invoke([
        HumanMessage(content="Write a Python function that returns the sum of two numbers. Return ONLY the code, no explanation.")
    ])
    
    print("SUCCESS! Groq API is working.")
    print("-" * 50)
    print("Model response:")
    print(response.content)
    print("-" * 50)

if __name__ == "__main__":
    test_groq_connection()
