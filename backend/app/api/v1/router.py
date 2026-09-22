from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_roles
from app.schemas.user import CurrentUser
from app.core.audit import audit_event

from app.llm.factory import get_llm_provider
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

from app.agents.workflow import agent_workflow
from app.schemas.agent import AgentRunRequest, AgentRunResponse

import uuid

from app.rag.container import repository_scope
from app.schemas.document import (
    DocumentIngestRequest,
    DocumentIngestResponse,
    DocumentSummary,
    RAGQueryRequest,
    RAGQueryResponse,
)
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.tools.registry import tool_registry
from app.embeddings.factory import get_embedding_provider
from app.evaluation.rag import RetrievalCase, evaluate_retrieval
from app.schemas.evaluation import (
    RetrievalEvaluationRequest,
    RetrievalEvaluationResponse,
)

api_router = APIRouter()


@api_router.get("/status", tags=["status"])
async def api_status():
    return {
        "status": "ok",
        "api_version": "v1",
    }

@api_router.post(
    "/documents",
    response_model=DocumentIngestResponse,
    tags=["documents"],
)
async def ingest_document(request: DocumentIngestRequest):
    with repository_scope() as repository:
        service = DocumentService(repository)
        return await service.ingest_document(request)


@api_router.get(
    "/documents",
    response_model=list[DocumentSummary],
    tags=["documents"],
)
async def list_documents():
    with repository_scope() as repository:
        return [
            DocumentSummary(
                document_id=document.document_id,
                title=document.title,
                status=document.status,
                created_at=document.created_at,
                embedding_provider=document.embedding_provider,
                embedding_model=document.embedding_model,
            )
            for document in repository.list_documents()
        ]


@api_router.post(
    "/rag/query",
    response_model=RAGQueryResponse,
    tags=["rag"],
)
async def query_knowledge(request: RAGQueryRequest):
    with repository_scope() as repository:
        service = RAGService(repository)
        return await service.answer(request.question, request.top_k)


@api_router.get("/tools", tags=["tools"])
async def list_tools():
    return {
        "tools": [
            {
                "name": definition.name,
                "description": definition.description,
                "permission": definition.permission.value,
                "requires_approval": definition.requires_approval,
            }
            for definition in tool_registry.values()
        ]
    }


@api_router.post(
    "/evals/retrieval",
    response_model=RetrievalEvaluationResponse,
    tags=["evaluation"],
)
async def run_retrieval_evaluation(request: RetrievalEvaluationRequest):
    cases = [
        RetrievalCase(
            question=case.question,
            expected_document_id=case.expected_document_id,
        )
        for case in request.cases
    ]
    with repository_scope() as repository:
        result = await evaluate_retrieval(
            repository,
            get_embedding_provider(),
            cases,
            request.top_k,
        )
    return RetrievalEvaluationResponse(
        case_count=result.case_count,
        hit_rate_at_k=result.hit_rate_at_k,
        mean_reciprocal_rank=result.mean_reciprocal_rank,
        failures=result.failures,
    )

@api_router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(request: ChatRequest):
    provider = get_llm_provider()
    service = ChatService(provider)
    return await service.chat(request)


@api_router.get("/me", tags=["users"])
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user


@api_router.get("/admin/status", tags=["admin"])
async def admin_status(
    current_user: CurrentUser = Depends(require_roles("admin")),
):
    audit_event(
        event="admin.status.accessed",
        outcome="success",
        actor_id=current_user.id,
    )

    return {
        "status": "ok",
        "admin": current_user.id,
    }


@api_router.post("/agent/run", response_model=AgentRunResponse, tags=["agents"])
async def run_agent(request: AgentRunRequest):
    thread_id = request.thread_id or str(uuid.uuid4())

    audit_event(
        event="agent.workflow.started",
        outcome="started",
        metadata={
            "workflow": "conditional-langgraph:v4",
            "thread_id": thread_id,
        },
    )

    result = await agent_workflow.ainvoke(
        {
            "user_message": request.message,
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    audit_event(
        event="agent.workflow.finished",
        outcome=result["status"],
        metadata={
            "workflow": "conditional-langgraph:v4",
            "thread_id": thread_id,
            "route": result.get("route"),
        },
    )

    return AgentRunResponse(
        status=result["status"],
        answer=result.get("answer"),
        error=result.get("error"),
        approval_reason=result.get("approval_reason"),
        plan=result["plan"],
        workflow="conditional-langgraph:v4",
        route=result["route"],
        thread_id=thread_id,
        provider=result.get("provider"),
        model=result.get("model"),
        prompt_id=result.get("prompt_id"),
        latency_ms=result.get("latency_ms"),
        usage=result.get("usage"),
        citations=result.get("citations", []),
        retrieval_count=result.get("retrieval_count", 0),
        tool_name=result.get("tool_name"),
        tool_result=result.get("tool_result"),
    )
