# app/graph/edges.py
from app.graph.state import CodeForgeState


def should_repair_or_finish(state: CodeForgeState) -> str:
    """After critic: pass -> regression, fail -> repair or give up."""
    if state["is_correct"]:
        return "regression"
    if state.get("retry_count", 0) >= state.get("max_retries", 3):
        return "output"
    return "repair"


def should_repair_after_regression(state: CodeForgeState) -> str:
    """After regression: all passed -> output, any failed -> repair."""
    if state.get("regression_passed", True):
        return "output"
    if state.get("retry_count", 0) >= state.get("max_retries", 3):
        return "output"
    return "repair"