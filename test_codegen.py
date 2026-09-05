"""
Phase 3 test: LLM code generation + sandbox execution.
Full pipeline: English task -> plan -> code -> run -> output.
Run with: python test_codegen.py
"""
from app.llm.client import call_llm
from app.llm.prompts import PLAN_PROMPT, CODE_GEN_PROMPT
from app.sandbox.executor import execute_code

def test_codegen(task: str):
    print(f"TASK: {task}")
    print("-" * 60)

    # Step 1: Generate a plan
    print("Step 1: Planning...")
    plan = call_llm(PLAN_PROMPT.format(task=task))
    print(f"Plan:\n{plan}\n")

    # Step 2: Generate code from plan
    print("Step 2: Generating code...")
    code = call_llm(CODE_GEN_PROMPT.format(task=task, plan=plan))
    print(f"Code:\n{code}\n")

    # Step 3: Run code in sandbox
    print("Step 3: Executing in sandbox...")
    result = execute_code(code)
    print(f"stdout   : {result['stdout'].strip()}")
    print(f"stderr   : {result['stderr'].strip()[:200]}")
    print(f"exit_code: {result['exit_code']}")
    print(f"timed_out: {result['timed_out']}")
    print("-" * 60)
    return result

if __name__ == "__main__":
    # Test 1: Simple arithmetic
    test_codegen("Write a function that returns the sum of all numbers from 1 to N, then print the result for N=100")

    print()

    # Test 2: String manipulation
    test_codegen("Write a function that checks if a string is a palindrome, then test it with the word 'racecar'")
