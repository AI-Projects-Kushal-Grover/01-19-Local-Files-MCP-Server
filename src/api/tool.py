from src.mcp_instance import mcp

@mcp.tool("files/list")
async def list_files() -> list[str]:
    return []

@mcp.tool("files/search")
async def search_files() -> list[str]:
    return []

@mcp.tool("file/read")
async def read_file() -> str:
    return ""

@mcp.tool("file/info")
async def file_info() -> str:
    return ""
