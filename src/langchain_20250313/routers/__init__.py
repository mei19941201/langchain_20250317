from fastapi import FastAPI

from .openai import v1_api


def register_router(app: FastAPI):
    app.include_router(v1_api)