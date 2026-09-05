# app/graph/state.py
# CodeForgeState is the shared "memory" passed between every node.
# Think of it as a lab notebook — every node reads from it and writes to it.
# TypedDict means every key has a declared type — no surprises.

from typing import TypedDict, List

class CodeForgeState(TypedDict):
    # Input
    task: str                        # The plain English task
    task_id: str                     # Unique ID for this run

    # Planning
    plan: str                        # LLM-generated plan

    # Code
    code: str                        # Current code attempt

    # Execution results
    stdout: str                      # Container stdout
    stderr: str                      # Container stderr
    exit_code: int                   # 0 = success
    timed_out: bool                  # True if killed after 10s

    # Critic decision
    is_correct: bool                 # Did it produce correct output?
    error_type: str                  # "none" | "syntax" | "runtime" | "timeout"

    # Self-repair tracking
    retry_count: int                 # How many repair attempts so far
    max_retries: int                 # Always 3
    repair_history: List[dict]       # Log of every attempt

    # Final output
    final_code: str                  # The working code
    final_output: str                # The correct output
    success: bool                    # Overall success/failure
    total_iterations: int            # How many attempts total
    execution_trace: List[dict]      # Full log of every attempt
