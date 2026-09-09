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

api_router = APIRouter()


@api_router.get("/status", tags=["status"])
async def api_status():
    return {
        "status": "ok",
        "api_version": "v1",
    }

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

    return AgentRunResponse(
        status=result["status"],
        answer=result.get("answer"),
        error=result.get("error"),
        plan=result["plan"],
        workflow="conditional-langgraph:v2",
        route=result["route"],
        thread_id=thread_id,
        provider=result.get("provider"),
        model=result.get("model"),
        prompt_id=result.get("prompt_id"),
        latency_ms=result.get("latency_ms"),
        usage=result.get("usage"),
    )