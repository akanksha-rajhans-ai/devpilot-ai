from typing import Any


class MCPToolClient:
    def __init__(self, server_url: str):
        if not server_url:
            raise ValueError("MCP server URL is required")
        self.server_url = server_url

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            from mcp import Client
        except ImportError as exc:
            raise RuntimeError("Install the mcp package to use remote MCP tools") from exc

        async with Client(self.server_url) as client:
            result = await client.call_tool(name, arguments)
            return result.structured_content or {"content": str(result.content)}
