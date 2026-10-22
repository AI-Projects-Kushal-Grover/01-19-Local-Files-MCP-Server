from src.mcp_instance import mcp
from src.services.filesystem import (
    file_info as get_file_info,
    list_files as get_files,
    read_file as get_file,
    search_files as find_files,
)

@mcp.resource("files://file/list")
async def list_files() -> list[str]:
    return get_files()

@mcp.resource("files://file/search/{query}")
async def search_files(query: str) -> list[str]:
    return find_files(query)

@mcp.resource("file://read/{path}")
async def read_file(path: str) -> str:
    return get_file(path)

@mcp.resource("file://info/{path}")
async def file_info(path: str) -> dict[str, str | int]:
    return get_file_info(path)
