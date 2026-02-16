from langgraph.graph import StateGraph, START, END

from .state import AgentState

from .nodes import (
    planner_node,
    writer_node,
    loader_node,
    executor_node,
    debugger_node,
    decision_node
)


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)

    graph.add_node("writer", writer_node)

    graph.add_node("loader", loader_node)

    graph.add_node("executor", executor_node)

    graph.add_node("debugger", debugger_node)

    graph.add_edge(START, "planner")

    graph.add_edge("planner", "writer")

    graph.add_edge("writer", "loader")

    graph.add_edge("loader", "executor")

    graph.add_conditional_edges(
        "executor",
        decision_node,
        {
            "debug": "debugger",
            "end": END
        }
    )

    graph.add_edge("debugger", "writer")

    return graph.compile()


agent = build_graph()
