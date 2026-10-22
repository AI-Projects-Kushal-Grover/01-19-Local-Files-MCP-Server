from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.file import router as file_router
from src.services.mcp_client import MCPClient

env_file = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_file)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp_client = MCPClient()
    await mcp_client.start()
    app.state.mcp_client = mcp_client
    try:
        yield
    finally:
        await mcp_client.close()


app = FastAPI(
    title="file-system-mcp-client",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(file_router)
