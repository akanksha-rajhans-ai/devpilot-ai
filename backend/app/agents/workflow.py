from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.observability.llm import record_llm_call
from app.prompts.registry import get_prompt_template


def plan_node(state: AgentState) -> AgentState:
    user_message = state["user_message"]

    return {
        "plan": f"Understand the user request and produce a clear answer: {user_message}"
    }


async def answer_node(state: AgentState) -> AgentState:
    prompt_template = get_prompt_template("agent.answer")

    prompt = prompt_template.render(
        plan=state["plan"],
        message=state["user_message"],
    )

    provider = get_llm_provider()
    result = await provider.generate(prompt)

    record_llm_call(
        prompt_id=prompt_template.prompt_id,
        result=result,
        metadata={"workflow": "minimal-langgraph:v2"},
    )

    return {
        "answer": result.content,
        "provider": result.provider,
        "model": result.model,
        "prompt_id": prompt_template.prompt_id,
        "latency_ms": result.latency_ms,
        "usage": result.usage,
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