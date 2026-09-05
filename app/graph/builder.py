# app/graph/builder.py
from langgraph.graph import StateGraph, END
from app.graph.state import CodeForgeState
from app.graph.nodes import (
    plan_node, code_node, sandbox_node,
    critic_node, repair_node, regression_node, output_node
)
from app.graph.edges import should_repair_or_finish, should_repair_after_regression


def build_graph():
    graph = StateGraph(CodeForgeState)

    graph.add_node("node_plan", plan_node)
    graph.add_node("node_code", code_node)
    graph.add_node("node_sandbox", sandbox_node)
    graph.add_node("node_critic", critic_node)
    graph.add_node("node_repair", repair_node)
    graph.add_node("node_regression", regression_node)
    graph.add_node("node_output", output_node)

    graph.add_edge("node_plan", "node_code")
    graph.add_edge("node_code", "node_sandbox")
    graph.add_edge("node_sandbox", "node_critic")
    graph.add_edge("node_repair", "node_sandbox")

    graph.add_conditional_edges(
        "node_critic",
        should_repair_or_finish,
        {
            "regression": "node_regression",
            "repair": "node_repair",
            "output": "node_output"
        }
    )

    graph.add_conditional_edges(
        "node_regression",
        should_repair_after_regression,
        {
            "output": "node_output",
            "repair": "node_repair"
        }
    )

    graph.set_entry_point("node_plan")
    graph.add_edge("node_output", END)

    return graph.compile()


codeforge_graph = build_graph()