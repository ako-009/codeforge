# app/graph/nodes.py
# Each function here is one node in the LangGraph graph.
# A node receives the full state, does its job, and returns
# a dict of keys to UPDATE in the state.

import uuid
from app.llm.client import call_llm
from app.llm.prompts import PLAN_PROMPT, CODE_GEN_PROMPT, REPAIR_PROMPT
from app.sandbox.executor import execute_code
from app.graph.state import CodeForgeState


def plan_node(state: CodeForgeState) -> dict:
    """
    Node 1: Ask LLM to plan the approach for the task.
    Input : state["task"]
    Output: state["plan"]
    """
    plan = call_llm(PLAN_PROMPT.format(task=state["task"]))
    return {"plan": plan}


def code_node(state: CodeForgeState) -> dict:
    """
    Node 2: Ask LLM to write code based on the task and plan.
    Input : state["task"], state["plan"]
    Output: state["code"]
    """
    code = call_llm(CODE_GEN_PROMPT.format(
        task=state["task"],
        plan=state["plan"]
    ))
    return {"code": code}


def sandbox_node(state: CodeForgeState) -> dict:
    """
    Node 3: Run current code in Docker sandbox.
    Input : state["code"]
    Output: state["stdout"], state["stderr"], state["exit_code"], state["timed_out"]
    Also appends this attempt to execution_trace.
    """
    result = execute_code(state["code"])

    # Record this attempt in the trace
    trace_entry = {
        "attempt": state.get("retry_count", 0) + 1,
        "code": state["code"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"]
    }

    trace = state.get("execution_trace", [])
    trace.append(trace_entry)

    return {
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"],
        "execution_trace": trace
    }


def critic_node(state: CodeForgeState) -> dict:
    """
    Node 4: Decide if the output is correct.
    Simple heuristic: exit_code 0 and no timeout = correct.
    Input : state["exit_code"], state["timed_out"], state["stderr"]
    Output: state["is_correct"], state["error_type"]
    """
    if state["timed_out"]:
        return {"is_correct": False, "error_type": "timeout"}
    if state["exit_code"] != 0:
        stderr = state.get("stderr", "")
        if "SyntaxError" in stderr:
            return {"is_correct": False, "error_type": "syntax"}
        return {"is_correct": False, "error_type": "runtime"}
    return {"is_correct": True, "error_type": "none"}


def repair_node(state: CodeForgeState) -> dict:
    """
    Node 5: Ask LLM to fix the broken code.
    Shows the LLM: original task + broken code + error message.
    Input : state["task"], state["code"], state["stderr"], state["stdout"]
    Output: state["code"] (updated), state["retry_count"] (incremented)
    """
    attempt = state.get("retry_count", 0) + 1

    fixed_code = call_llm(REPAIR_PROMPT.format(
        task=state["task"],
        attempt=attempt,
        code=state["code"],
        stderr=state["stderr"],
        stdout=state["stdout"]
    ))

    # Log this repair in history
    history = state.get("repair_history", [])
    history.append({
        "attempt": attempt,
        "broken_code": state["code"],
        "error": state["stderr"],
        "fixed_code": fixed_code
    })

    return {
        "code": fixed_code,
        "retry_count": attempt,
        "repair_history": history
    }


def output_node(state: CodeForgeState) -> dict:
    """
    Node 6: Package the final result.
    Input : full state
    Output: final_code, final_output, success, total_iterations
    """
    return {
        "final_code": state["code"],
        "final_output": state["stdout"],
        "success": state["is_correct"],
        "total_iterations": state.get("retry_count", 0) + 1
    }
