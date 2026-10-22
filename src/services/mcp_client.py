import json
import sys
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class MCPClient:
    def __init__(self) -> None:
        self._exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None

    async def start(self) -> None:
        server = StdioServerParameters(
            command=sys.executable,
            args=["-m", "src.mcp_server"],
            cwd=str(Path(__file__).resolve().parents[2]),
        )
        try:
            read_stream, write_stream = await self._exit_stack.enter_async_context(
                stdio_client(server)
            )
            self.session = await self._exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            await self.session.initialize()
        except BaseException:
            await self._exit_stack.aclose()
            raise

    async def close(self) -> None:
        await self._exit_stack.aclose()
        self.session = None

    def _session(self) -> ClientSession:
        if self.session is None:
            raise RuntimeError("MCP client has not been started.")
        return self.session

    async def list_tools(self) -> list[dict[str, Any]]:
        result = await self._session().list_tools()
        return [tool.model_dump(mode="json") for tool in result.tools]

    async def list_resources(self) -> list[dict[str, Any]]:
        result = await self._session().list_resources()
        return [resource.model_dump(mode="json") for resource in result.resources]

    async def call_tool(
        self, tool_name: str, arguments: dict[str, Any] | None = None
    ) -> Any:
        result = await self._session().call_tool(tool_name, arguments or {})
        if result.is_error:
            message = "; ".join(
                item.text for item in result.content if hasattr(item, "text")
            )
            raise RuntimeError(f"MCP tool {tool_name!r} failed: {message}")
        if result.structured_content is not None:
            if set(result.structured_content) == {"result"}:
                return result.structured_content["result"]
            return result.structured_content
        if result.content and hasattr(result.content[0], "text"):
            text = result.content[0].text
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
        return result.content
