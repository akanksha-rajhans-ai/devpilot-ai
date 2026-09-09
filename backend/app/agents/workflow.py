from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.observability.llm import record_llm_call
from app.prompts.registry import get_prompt_template

from app.llm.errors import LLMProviderError
from app.schemas.llm import LLMResult, LLMUsage
from langgraph.types import RetryPolicy

def should_retry_provider_error(exc: Exception) -> bool:
    return isinstance(exc, LLMProviderError) and exc.retryable

def provider_failure_state(
    exc: LLMProviderError,
    route: str,
    prompt_id: str,
) -> AgentState:
    failure_result = LLMResult(
        content="",
        provider=exc.provider,
        model=exc.model,
        latency_ms=0,
        usage=LLMUsage(),
    )

    record_llm_call(
        prompt_id=prompt_id,
        result=failure_result,
        outcome="failure",
        metadata={
            "workflow": "conditional-langgraph:v2",
            "route": route,
        },
    )

    return {
        "status": "failed",
        "route": route,
        "error": "AI provider is temporarily unavailable",
        "provider": exc.provider,
        "model": exc.model,
        "prompt_id": prompt_id,
        "latency_ms": 0,
        "usage": LLMUsage(),
    }


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

    try:
        result = await provider.generate(prompt)
    except LLMProviderError as exc:
        if exc.retryable:
            raise
        return provider_failure_state(
            exc=exc,
            route="code_explanation",
            prompt_id=prompt_template.prompt_id,
        )

    record_llm_call(
        prompt_id=prompt_template.prompt_id,
        result=result,
        metadata={
            "workflow": "conditional-langgraph:v2",
            "route": "code_explanation",
        },
    )

    return {
        "status": "completed",
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

    try:
        result = await provider.generate(prompt)
    except LLMProviderError as exc:
        if exc.retryable:
            raise
        return provider_failure_state(
            exc=exc,
            route="general_answer",
            prompt_id=prompt_template.prompt_id,
        )

    record_llm_call(
        prompt_id=prompt_template.prompt_id,
        result=result,
        metadata={
            "workflow": "conditional-langgraph:v2",
            "route": "general_answer",
        },
    )

    return {
        "status": "completed",
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
    graph_builder.add_node(
        "code_explanation",
        code_explanation_node,
        retry_policy=RetryPolicy(
            max_attempts=2,
            retry_on=should_retry_provider_error,
        ),
    )
    graph_builder.add_node(
        "general_answer",
        general_answer_node,
        retry_policy=RetryPolicy(
            max_attempts=2,
            retry_on=should_retry_provider_error,
        ),
    )

    graph_builder.add_edge(START, "plan")
    graph_builder.add_conditional_edges("plan", route_after_plan)
    graph_builder.add_edge("code_explanation", END)
    graph_builder.add_edge("general_answer", END)

    return graph_builder.compile()


agent_workflow = build_agent_workflow()