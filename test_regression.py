"""
Phase 5 test: Regression test runner.
Run with: python test_regression.py
"""
import uuid
from app.graph.builder import codeforge_graph


def run_agent(task: str, test_cases: list = []):
    print(f"TASK: {task}")
    print(f"Test cases: {len(test_cases)}")
    print("-" * 60)

    initial_state = {
        "task": task,
        "task_id": str(uuid.uuid4()),
        "test_cases": test_cases,
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
        "regression_passed": False,
        "regression_results": [],
        "final_code": "",
        "final_output": "",
        "success": False,
        "total_iterations": 0,
        "execution_trace": []
    }

    result = codeforge_graph.invoke(initial_state)

    print(f"Success            : {result['success']}")
    print(f"Total attempts     : {result['total_iterations']}")
    print(f"Regression passed  : {result['regression_passed']}")
    print(f"Final output       : {result['final_output'].strip()}")
    if result['regression_results']:
        for r in result['regression_results']:
            status = "PASS" if r['passed'] else "FAIL"
            print(f"  Test {r['test_case']}: {status} (expected={r['expected']}, actual={r['actual']})")
    print("-" * 60)
    return result


if __name__ == "__main__":
    # Test with no test cases (auto pass regression)
    run_agent("Write a Python function to compute the factorial of 5 and print the result")
    print()

    # Test with test cases provided
    run_agent(
        task="Write a Python function called main(n) that returns the factorial of n",
        test_cases=[
            {"input": "5", "expected": "120"},
            {"input": "10", "expected": "3628800"},
        ]
    )