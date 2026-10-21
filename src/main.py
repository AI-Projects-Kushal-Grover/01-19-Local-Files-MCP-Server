from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.file import router as file_router

env_file = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_file)

app = FastAPI(title="file-system-mcp-client", version="0.1.0")

app.include_router(file_router)
