# app/graph/edges.py
# Conditional edge functions — these decide which node to go to next.
# LangGraph calls these after critic_node to decide the next step.

from app.graph.state import CodeForgeState


def should_repair_or_finish(state: CodeForgeState) -> str:
    """
    After critic_node: did the code pass?
    - Yes ? go to output_node
    - No, but retries left ? go to repair_node
    - No, retries exhausted ? go to output_node anyway (best attempt)
    """
    if state["is_correct"]:
        return "output"
    if state.get("retry_count", 0) >= state.get("max_retries", 3):
        return "output"   # Give up after max retries
    return "repair"
