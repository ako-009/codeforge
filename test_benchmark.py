"""
Phase 7 test: HumanEval benchmark runner.
Runs 10 problems and prints metrics.
Run with: python test_benchmark.py
WARNING: Takes 2-5 minutes (10 LLM calls + sandbox runs).
"""
import json
from app.benchmark.runner import run_benchmark

if __name__ == "__main__":
    report = run_benchmark("data/humaneval_10.json")

    metrics = report["metrics"]
    print("\nBENCHMARK RESULTS")
    print("=" * 40)
    print(f"Total problems   : {metrics['total_problems']}")
    print(f"Passed           : {metrics['passed']}")
    print(f"Failed           : {metrics['failed']}")
    print(f"Completion rate  : {metrics['completion_rate']*100:.1f}%")
    print(f"First-try rate   : {metrics['first_try_rate']*100:.1f}%")
    print(f"Self-repair rate : {metrics['self_repair_rate']*100:.1f}%")
    print(f"Avg iterations   : {metrics['avg_iterations']}")
    print("=" * 40)

    # Save results to file
    with open("data/benchmark_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Results saved to data/benchmark_results.json")