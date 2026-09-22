from mcp.server import MCPServer

from app.tools.executor import execute_tool


mcp = MCPServer("DevPilot AI Knowledge Tools")


@mcp.tool()
async def list_documents(limit: int = 20) -> dict:
    """List documents currently available to the DevPilot knowledge base."""
    return await execute_tool("list_documents", {"limit": limit}, actor_id="mcp")


@mcp.tool()
async def search_knowledge(query: str, top_k: int = 4) -> dict:
    """Search indexed document chunks and return evidence with similarity scores."""
    return await execute_tool(
        "search_knowledge",
        {"query": query, "top_k": top_k},
        actor_id="mcp",
    )
