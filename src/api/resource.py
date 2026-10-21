from src.mcp_instance import mcp

@mcp.resource("files://file/list")
async def list_files() -> list[str]:
    return []

@mcp.resource("files://file/search/{query}")
async def search_files(query: str) -> list[str]:
    return []

@mcp.resource("file://read/{path}")
async def read_file(path: str) -> str:
    return ""

@mcp.resource("file://info/{path}")
async def file_info(path: str) -> str:
    return ""
