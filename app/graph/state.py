# app/graph/state.py
from typing import TypedDict, List, Optional

class CodeForgeState(TypedDict):
    # Input
    task: str
    task_id: str
    test_cases: List[dict]           # [{"input": "...", "expected": "..."}]

    # Planning
    plan: str

    # Code
    code: str

    # Execution results
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool

    # Critic decision
    is_correct: bool
    error_type: str

    # Self-repair tracking
    retry_count: int
    max_retries: int
    repair_history: List[dict]

    # Regression
    regression_passed: bool
    regression_results: List[dict]   # Per-test-case results

    # Final output
    final_code: str
    final_output: str
    success: bool
    total_iterations: int
    execution_trace: List[dict]