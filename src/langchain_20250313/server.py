import uvicorn
import colorama
from fastapi import FastAPI

from .routers import register_router


def server():
    colorama.init(autoreset=True)
    app = FastAPI(
        title="langchain-20250313"
    )
    register_router(app)
    uvicorn.run(app, port=11434)
