from dataclasses import dataclass
from enum import Enum


class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    SENSITIVE = "sensitive"


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    permission: ToolPermission
    requires_approval: bool


tool_registry = {
    "list_documents": ToolDefinition(
        name="list_documents",
        description="List documents available in the DevPilot knowledge base.",
        permission=ToolPermission.READ,
        requires_approval=False,
    ),
    "search_knowledge": ToolDefinition(
        name="search_knowledge",
        description="Search the DevPilot knowledge base for relevant chunks.",
        permission=ToolPermission.READ,
        requires_approval=False,
    ),
}


def authorize_tool(tool_name: str, approved: bool = False) -> ToolDefinition:
    try:
        definition = tool_registry[tool_name]
    except KeyError as exc:
        raise ValueError(f"Unknown tool: {tool_name}") from exc

    if definition.requires_approval and not approved:
        raise PermissionError(f"Tool requires approval: {tool_name}")

    return definition
