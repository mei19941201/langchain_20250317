import asyncio
from time import time
from pydantic import BaseModel, Field
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from langchain_20250313.core import logger, llm


class Delta(BaseModel):
    role: str = Field("assistent")
    content: str


class Choice(BaseModel):
    index: int = Field(0)
    delta: Delta
    finish_reason: None | str = Field(None)


class ResponseChunk(BaseModel):
    id: str
    obj: str = Field("chat.completion.chunk")
    created: int
    model: str
    system_fingerprint: str
    choices: list[Choice]



v1_api = APIRouter(prefix="/v1", tags=["v1"])


async def llm_chat(content: str):
    async for i in llm.astream(content):
        js_i = i.model_dump()
        response_metadata = js_i["response_metadata"]
        res_chunk = ResponseChunk(
            id=js_i["id"],
            created=int(time()),
            model=response_metadata.get("model_name", ""),
            system_fingerprint=response_metadata.get("system_fingerprint", ""),
            choices=[
                Choice(
                    delta=Delta(
                        content=js_i["content"],
                    ),
                    finish_reason = None if len(response_metadata)==0 else response_metadata["finish_reason"]
                )
            ]
        )
        yield res_chunk.model_dump_json()
    yield "[DONE]"


@v1_api.post("/chat/completions")
async def chat_completions(
    res: dict
):  
    content = res["messages"][-1]["content"]
    logger.info(res)
    return EventSourceResponse(llm_chat(content))