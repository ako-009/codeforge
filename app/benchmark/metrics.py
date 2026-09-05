# app/benchmark/metrics.py

def compute_metrics(results: list) -> dict:
    total = len(results)
    if total == 0:
        return {}

    passed = sum(1 for r in results if r["success"])
    first_try = sum(1 for r in results if r["success"] and r["total_iterations"] == 1)
    repaired = sum(1 for r in results if r["success"] and r["total_iterations"] > 1)
    timed_out = sum(1 for r in results if r.get("timed_out", False))

    return {
        "total_problems": total,
        "passed": passed,
        "failed": total - passed,
        "completion_rate": round(passed / total, 3),
        "first_try_rate": round(first_try / total, 3),
        "self_repair_rate": round(repaired / max(total - first_try, 1), 3),
        "avg_iterations": round(sum(r["total_iterations"] for r in results) / total, 2),
        "timeout_rate": round(timed_out / total, 3)
    }