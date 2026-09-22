from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.observability.llm import record_llm_call
from app.prompts.registry import get_prompt_template

from app.llm.errors import LLMProviderError
from app.schemas.llm import LLMResult, LLMUsage
from langgraph.types import RetryPolicy

from langgraph.checkpoint.memory import InMemorySaver

from app.rag.container import repository_scope
from app.services.rag_service import RAGService
from app.tools.executor import execute_tool

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
            "workflow": "conditional-langgraph:v4",
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


def route_after_plan(
    state: AgentState,
) -> Literal[
    "needs_approval",
    "knowledge_answer",
    "tool_action",
    "code_review",
    "debug",
    "documentation",
    "code_generation",
    "code_explanation",
    "general_answer",
]:
    message = state["user_message"].lower()

    risky_keywords = [
        "delete",
        "drop",
        "remove",
        "deploy",
        "production",
        "prod",
        "credential",
        "secret",
        "token",
        "password",
        "post to slack",
        "comment on pr",
    ]

    if any(keyword in message for keyword in risky_keywords):
        return "needs_approval"

    knowledge_keywords = [
        "according to",
        "based on the document",
        "based on our docs",
        "knowledge base",
        "documentation says",
        "rag",
        "uploaded document",
    ]

    if any(keyword in message for keyword in knowledge_keywords):
        return "knowledge_answer"

    tool_keywords = ["list documents", "show documents", "knowledge inventory"]
    if any(keyword in message for keyword in tool_keywords):
        return "tool_action"

    if any(keyword in message for keyword in ["stack trace", "exception", "debug", "root cause"]):
        return "debug"

    if any(keyword in message for keyword in ["review this", "code review", "review my"]):
        return "code_review"

    if any(keyword in message for keyword in ["write documentation", "write docs", "readme"]):
        return "documentation"

    if any(keyword in message for keyword in ["generate code", "implement", "build an api"]):
        return "code_generation"

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


async def knowledge_answer_node(state: AgentState) -> AgentState:
    with repository_scope() as repository:
        result = await RAGService(repository).answer(state["user_message"])

    return {
        "status": "completed",
        "route": "knowledge_answer",
        "answer": result.answer,
        "citations": [citation.model_dump() for citation in result.citations],
        "retrieval_count": result.retrieval_count,
        "provider": result.provider,
        "model": result.model,
        "prompt_id": result.prompt_id,
    }


async def tool_action_node(state: AgentState) -> AgentState:
    result = await execute_tool("list_documents", {}, actor_id="agent")
    document_titles = [document["title"] for document in result["documents"]]
    answer = (
        "Available knowledge documents: " + ", ".join(document_titles)
        if document_titles
        else "The knowledge base is currently empty."
    )
    return {
        "status": "completed",
        "route": "tool_action",
        "answer": answer,
        "tool_name": "list_documents",
        "tool_result": result,
    }


def needs_approval_node(state: AgentState) -> AgentState:
    return {
        "status": "waiting_for_approval",
        "route": "needs_approval",
        "approval_reason": "Request may perform a sensitive or irreversible action.",
        "answer": None,
    }



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
            "workflow": "conditional-langgraph:v4",
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


async def run_specialist_node(
    state: AgentState,
    route: str,
    prompt_name: str,
) -> AgentState:
    prompt_template = get_prompt_template(prompt_name)
    prompt = prompt_template.render(plan=state["plan"], message=state["user_message"])
    provider = get_llm_provider()

    try:
        result = await provider.generate(prompt)
    except LLMProviderError as exc:
        if exc.retryable:
            raise
        return provider_failure_state(exc, route, prompt_template.prompt_id)

    record_llm_call(
        prompt_id=prompt_template.prompt_id,
        result=result,
        metadata={"workflow": "conditional-langgraph:v4", "route": route},
    )
    return {
        "status": "completed",
        "route": route,
        "answer": result.content,
        "provider": result.provider,
        "model": result.model,
        "prompt_id": prompt_template.prompt_id,
        "latency_ms": result.latency_ms,
        "usage": result.usage,
    }


async def code_review_node(state: AgentState) -> AgentState:
    return await run_specialist_node(state, "code_review", "agent.code_review")


async def debug_node(state: AgentState) -> AgentState:
    return await run_specialist_node(state, "debug", "agent.debug")


async def documentation_node(state: AgentState) -> AgentState:
    return await run_specialist_node(state, "documentation", "agent.documentation")


async def code_generation_node(state: AgentState) -> AgentState:
    return await run_specialist_node(
        state,
        "code_generation",
        "agent.code_generation",
    )


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
            "workflow": "conditional-langgraph:v4",
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

    graph_builder.add_node("needs_approval", needs_approval_node)
    graph_builder.add_node("knowledge_answer", knowledge_answer_node)
    graph_builder.add_node("tool_action", tool_action_node)

    specialist_nodes = {
        "code_review": code_review_node,
        "debug": debug_node,
        "documentation": documentation_node,
        "code_generation": code_generation_node,
    }
    for name, node in specialist_nodes.items():
        graph_builder.add_node(
            name,
            node,
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
    graph_builder.add_edge("knowledge_answer", END)
    graph_builder.add_edge("tool_action", END)
    for name in specialist_nodes:
        graph_builder.add_edge(name, END)
    graph_builder.add_edge("needs_approval", END)


    checkpointer = InMemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)


agent_workflow = build_agent_workflow()
