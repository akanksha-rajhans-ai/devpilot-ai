from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.observability.llm import record_llm_call
from app.prompts.registry import get_prompt_template


def plan_node(state: AgentState) -> AgentState:
    user_message = state["user_message"]

    return {
        "plan": f"Classify the request and answer clearly: {user_message}"
    }


def route_after_plan(state: AgentState) -> Literal["code_explanation", "general_answer"]:
    message = state["user_message"].lower()

    code_keywords = [
        "code",
        "function",
        "class",
        "api",
        "bug",
        "error",
        "stack trace",
        "python",
        "java",
        "fastapi",
        "langgraph",
    ]

    if any(keyword in message for keyword in code_keywords):
        return "code_explanation"

    return "general_answer"


async def code_explanation_node(state: AgentState) -> AgentState:
    prompt_template = get_prompt_template("agent.code_explanation")

    prompt = prompt_template.render(
        plan=state["plan"],
        message=state["user_message"],
    )

    provider = get_llm_provider()
    result = await provider.generate(prompt)

    record_llm_call(
        prompt_id=prompt_template.prompt_id,
        result=result,
        metadata={
            "workflow": "conditional-langgraph:v1",
            "route": "code_explanation",
        },
    )

    return {
        "route": "code_explanation",
        "answer": result.content,
        "provider": result.provider,
        "model": result.model,
        "prompt_id": prompt_template.prompt_id,
        "latency_ms": result.latency_ms,
        "usage": result.usage,
    }


async def general_answer_node(state: AgentState) -> AgentState:
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
        metadata={
            "workflow": "conditional-langgraph:v1",
            "route": "general_answer",
        },
    )

    return {
        "route": "general_answer",
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
    graph_builder.add_node("code_explanation", code_explanation_node)
    graph_builder.add_node("general_answer", general_answer_node)

    graph_builder.add_edge(START, "plan")
    graph_builder.add_conditional_edges("plan", route_after_plan)
    graph_builder.add_edge("code_explanation", END)
    graph_builder.add_edge("general_answer", END)

    return graph_builder.compile()


agent_workflow = build_agent_workflow()