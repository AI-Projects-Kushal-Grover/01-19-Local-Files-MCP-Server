from fastapi import APIRouter, Request

from src.services.mcp_client import MCPClient

router = APIRouter()


@router.get("/files/list")
async def list_files(request: Request) -> list[str]:
    return await _client(request).call_tool("files-list")


@router.get("/files/search")
async def search_files(request: Request, query: str) -> list[str]:
    return await _client(request).call_tool("files-search", {"query": query})


@router.get("/file/read")
async def read_file(request: Request, file_name: str) -> str:
    return await _client(request).call_tool("file-read", {"path": file_name})


@router.get("/file/info")
async def file_info(request: Request, file_name: str) -> dict[str, str | int]:
    return await _client(request).call_tool("file-info", {"path": file_name})


@router.get("/mcp/tools-resources")
async def list_mcp_tools_resources(request: Request) -> dict[str, list[dict]]:
    client = _client(request)
    tools = await client.list_tools()
    resources = await client.list_resources()
    return {"tools": tools, "resources": resources}


def _client(request: Request) -> MCPClient:
    return request.app.state.mcp_client
