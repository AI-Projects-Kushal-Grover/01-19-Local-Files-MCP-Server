from src.mcp_instance import mcp
from src.services.filesystem import (
    file_info as get_file_info,
    list_files as get_files,
    read_file as get_file,
    search_files as find_files,
)

@mcp.tool("files-list")
async def list_files() -> list[str]:
    return get_files()

@mcp.tool("files-search")
async def search_files(query: str) -> list[str]:
    return find_files(query)

@mcp.tool("file-read")
async def read_file(path: str) -> str:
    return get_file(path)

@mcp.tool("file-info")
async def file_info(path: str) -> dict[str, str | int]:
    return get_file_info(path)
