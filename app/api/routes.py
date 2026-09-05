# app/api/routes.py
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.graph.builder import codeforge_graph

router = APIRouter()

# In-memory store for task history (resets on server restart)
task_history = {}


# --- Request / Response models ---

class TestCase(BaseModel):
    input: str
    expected: str

class ExecuteRequest(BaseModel):
    task: str
    test_cases: Optional[List[TestCase]] = []

class ExecuteResponse(BaseModel):
    task_id: str
    task: str
    success: bool
    final_output: str
    final_code: str
    total_iterations: int
    regression_passed: bool
    execution_trace: list
    repair_history: list


# --- Endpoints ---

@router.post("/execute", response_model=ExecuteResponse)
def execute_task(request: ExecuteRequest):
    """
    Main endpoint. Receives a task, runs the full agent loop,
    returns code + output + trace.
    """
    task_id = str(uuid.uuid4())

    test_cases = [
        {"input": tc.input, "expected": tc.expected}
        for tc in (request.test_cases or [])
    ]

    initial_state = {
        "task": request.task,
        "task_id": task_id,
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

    # Store in history
    task_history[task_id] = result

    return ExecuteResponse(
        task_id=task_id,
        task=request.task,
        success=result["success"],
        final_output=result["final_output"],
        final_code=result["final_code"],
        total_iterations=result["total_iterations"],
        regression_passed=result["regression_passed"],
        execution_trace=result["execution_trace"],
        repair_history=result["repair_history"]
    )


@router.get("/task/{task_id}")
def get_task(task_id: str):
    """Get full result for a previously run task."""
    if task_id not in task_history:
        return {"error": "Task not found"}
    return task_history[task_id]


@router.get("/history")
def get_history():
    """List all past tasks and their outcomes."""
    return [
        {
            "task_id": tid,
            "task": r["task"],
            "success": r["success"],
            "total_iterations": r["total_iterations"]
        }
        for tid, r in task_history.items()
    ]


@router.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "CodeForge"}