from typing import Any

from app.core.audit import audit_event
from app.core.config import get_settings
from app.embeddings.factory import get_embedding_provider
from app.rag.container import repository_scope
from app.tools.registry import authorize_tool


async def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
    actor_id: str = "agent",
    approved: bool = False,
) -> dict[str, Any]:
    definition = authorize_tool(tool_name, approved=approved)
    audit_event(
        event="tool.execution.started",
        outcome="started",
        actor_id=actor_id,
        metadata={"tool": tool_name, "permission": definition.permission.value},
    )

    try:
        if tool_name == "list_documents":
            limit = max(1, min(int(arguments.get("limit", 20)), 100))
            with repository_scope() as repository:
                documents = repository.list_documents(limit=limit)
            result = {
                "documents": [
                    {
                        "document_id": document.document_id,
                        "title": document.title,
                        "status": document.status,
                    }
                    for document in documents
                ]
            }
        elif tool_name == "search_knowledge":
            query = str(arguments.get("query", "")).strip()
            if not query:
                raise ValueError("query is required")
            top_k = max(1, min(int(arguments.get("top_k", 4)), 10))
            embedding = (await get_embedding_provider().embed([query]))[0]
            settings = get_settings()
            with repository_scope() as repository:
                matches = repository.search_chunks(
                    embedding,
                    top_k,
                    0.0,
                    embedding_provider=settings.embedding_provider,
                    embedding_model=settings.embedding_model,
                )
            result = {
                "matches": [
                    {
                        "document_id": match.chunk.document_id,
                        "document_title": match.document_title,
                        "chunk_id": match.chunk.chunk_id,
                        "content": match.chunk.content,
                        "score": round(match.score, 4),
                    }
                    for match in matches
                ]
            }
        else:
            raise ValueError(f"No executor registered for tool: {tool_name}")
    except Exception:
        audit_event(
            event="tool.execution.finished",
            outcome="failure",
            actor_id=actor_id,
            metadata={"tool": tool_name},
        )
        raise

    audit_event(
        event="tool.execution.finished",
        outcome="success",
        actor_id=actor_id,
        metadata={"tool": tool_name},
    )
    return result
