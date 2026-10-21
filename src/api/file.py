from fastapi import APIRouter

router = APIRouter()

@router.get("files/list")
async def list_files() -> list[str]:
    return []

@router.get("files/search")
async def search_files(query: str) -> list[str]:
    return []

@router.get("file/read")
async def read_file(file_name: str) -> str:
    return ""

@router.get("file/info")
async def file_info(file_name: str) -> str:
    return ""
