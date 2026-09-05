# app/benchmark/runner.py
import json
import uuid
import time
from app.graph.builder import codeforge_graph
from app.benchmark.metrics import compute_metrics


def run_benchmark(data_path: str = "data/humaneval_10.json") -> dict:
    """
    Run all problems in the benchmark file through the CodeForge agent.
    Returns metrics dict.
    """
    with open(data_path, "r") as f:
        problems = json.load(f)

    results = []
    print(f"Running benchmark on {len(problems)} problems...")
    print("-" * 60)

    for i, problem in enumerate(problems):
        task_id = problem["task_id"]
        task = problem["prompt"]
        expected = problem["expected_output"].strip()

        print(f"[{i+1}/{len(problems)}] {task_id} ... ", end="", flush=True)
        start = time.time()

        initial_state = {
            "task": task,
            "task_id": str(uuid.uuid4()),
            "test_cases": [],
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

        try:
            result = codeforge_graph.invoke(initial_state)
            actual = result["final_output"].strip()
            success = (actual == expected)
            elapsed = round(time.time() - start, 1)

            results.append({
                "task_id": task_id,
                "success": success,
                "total_iterations": result["total_iterations"],
                "timed_out": result.get("timed_out", False),
                "expected": expected,
                "actual": actual,
                "elapsed_seconds": elapsed
            })

            status = "PASS" if success else "FAIL"
            print(f"{status} ({result['total_iterations']} iter, {elapsed}s)")

        except Exception as e:
            elapsed = round(time.time() - start, 1)
            results.append({
                "task_id": task_id,
                "success": False,
                "total_iterations": 0,
                "timed_out": False,
                "expected": expected,
                "actual": "",
                "elapsed_seconds": elapsed
            })
            print(f"ERROR: {e}")

    print("-" * 60)
    metrics = compute_metrics(results)
    return {"metrics": metrics, "results": results}