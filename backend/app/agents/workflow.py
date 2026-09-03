from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState


def plan_node(state: AgentState) -> AgentState:
    user_message = state["user_message"]

    return {
        "plan": f"Understand the user request and produce a clear answer: {user_message}"
    }


def answer_node(state: AgentState) -> AgentState:
    user_message = state["user_message"]
    plan = state["plan"]

    return {
        "answer": (
            "LangGraph workflow completed. "
            f"Plan: {plan}. "
            f"Original request: {user_message}"
        )
    }


def build_agent_workflow():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("plan", plan_node)
    graph_builder.add_node("answer", answer_node)

    graph_builder.add_edge(START, "plan")
    graph_builder.add_edge("plan", "answer")
    graph_builder.add_edge("answer", END)

    return graph_builder.compile()


agent_workflow = build_agent_workflow()