import pytest

from app.rag.document_store import document_store
from app.tools.executor import execute_tool
from app.tools.registry import authorize_tool


def test_unknown_tool_is_rejected():
    with pytest.raises(ValueError, match="Unknown tool"):
        authorize_tool("run_arbitrary_shell")


@pytest.mark.asyncio
async def test_list_documents_tool_is_bounded_and_read_only():
    document_store.clear()

    result = await execute_tool("list_documents", {"limit": 500})

    assert result == {"documents": []}
    assert authorize_tool("list_documents").requires_approval is False
