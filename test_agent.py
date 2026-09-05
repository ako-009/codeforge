"""
Phase 4 test: Full LangGraph agent loop.
Run with: python test_agent.py
"""
import uuid
from app.graph.builder import codeforge_graph


def run_agent(task: str):
    print(f"TASK: {task}")
    print("-" * 60)

    initial_state = {
        "task": task,
        "task_id": str(uuid.uuid4()),
        "plan": "",
        "code": "",
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "timed_out": False,
        "is_correct": False,
        "error_type": "none",
        "retry_count": 0,
        "max_retries": 3,
        "repair_history": [],
        "final_code": "",
        "final_output": "",
        "success": False,
        "total_iterations": 0,
        "execution_trace": []
    }

    result = codeforge_graph.invoke(initial_state)

    print(f"Success        : {result['success']}")
    print(f"Total attempts : {result['total_iterations']}")
    print(f"Final output   : {result['final_output'].strip()}")
    if result['repair_history']:
        print(f"Repairs made   : {len(result['repair_history'])}")
    print("-" * 60)
    return result


if __name__ == "__main__":
    run_agent("Write a Python function to compute the factorial of 10 and print the result")

    print()

    run_agent("Write a Python function that finds all prime numbers up to 50 and prints them")