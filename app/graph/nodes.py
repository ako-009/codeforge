# app/graph/nodes.py
from app.llm.client import call_llm
from app.llm.prompts import PLAN_PROMPT, CODE_GEN_PROMPT, REPAIR_PROMPT
from app.sandbox.executor import execute_code
from app.graph.state import CodeForgeState


def plan_node(state: CodeForgeState) -> dict:
    plan = call_llm(PLAN_PROMPT.format(task=state["task"]))
    return {"plan": plan}


def code_node(state: CodeForgeState) -> dict:
    code = call_llm(CODE_GEN_PROMPT.format(
        task=state["task"],
        plan=state["plan"]
    ))
    return {"code": code}


def sandbox_node(state: CodeForgeState) -> dict:
    result = execute_code(state["code"])

    trace_entry = {
        "attempt": state.get("retry_count", 0) + 1,
        "code": state["code"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"]
    }

    trace = list(state.get("execution_trace", []))
    trace.append(trace_entry)

    return {
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"],
        "execution_trace": trace
    }


def critic_node(state: CodeForgeState) -> dict:
    if state["timed_out"]:
        return {"is_correct": False, "error_type": "timeout"}
    if state["exit_code"] != 0:
        stderr = state.get("stderr", "")
        if "SyntaxError" in stderr:
            return {"is_correct": False, "error_type": "syntax"}
        return {"is_correct": False, "error_type": "runtime"}
    return {"is_correct": True, "error_type": "none"}


def repair_node(state: CodeForgeState) -> dict:
    attempt = state.get("retry_count", 0) + 1

    fixed_code = call_llm(REPAIR_PROMPT.format(
        task=state["task"],
        attempt=attempt,
        code=state["code"],
        stderr=state["stderr"],
        stdout=state["stdout"]
    ))

    history = list(state.get("repair_history", []))
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


def regression_node(state: CodeForgeState) -> dict:
    """
    Node 6: Run original test cases against the current code.
    Only triggered after a successful sandbox run.
    If no test cases provided, passes automatically.

    Each test case: {"input": "5", "expected": "120"}
    We wrap the code + input into a runner script and execute it.
    """
    test_cases = state.get("test_cases", [])

    # No test cases = auto pass
    if not test_cases:
        return {
            "regression_passed": True,
            "regression_results": []
        }

    results = []
    all_passed = True

    for i, tc in enumerate(test_cases):
        expected = str(tc.get("expected", "")).strip()
        input_val = tc.get("input", "")

        # Build a runner: inject the user's code + print output for input
        runner_code = f"""
{state['code']}

# Regression test runner
import sys
result = main({input_val})
print(result)
"""
        result = execute_code(runner_code)
        actual = result["stdout"].strip()
        passed = (actual == expected) and not result["timed_out"]

        results.append({
            "test_case": i + 1,
            "input": input_val,
            "expected": expected,
            "actual": actual,
            "passed": passed
        })

        if not passed:
            all_passed = False

    return {
        "regression_passed": all_passed,
        "regression_results": results
    }


def output_node(state: CodeForgeState) -> dict:
    return {
        "final_code": state["code"],
        "final_output": state["stdout"],
        "success": state["is_correct"] and state.get("regression_passed", True),
        "total_iterations": state.get("retry_count", 0) + 1
    }