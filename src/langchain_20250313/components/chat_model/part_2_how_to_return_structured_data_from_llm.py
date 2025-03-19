from langchain_20250313.core import llm, logger

from pydantic import BaseModel, Field
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables import RunnablePassthrough, RunnableParallel



class Joke(BaseModel):
    """
    将一个笑话给用户
    """
    setup: str = Field(..., description="The setup of the joke")
    punchline: str = Field(..., description="The punchline of the joke")
    rating: int | None = Field(None, description="How funny the joke is, from 1 to 10")


class CoversationalResponse(BaseModel):
    """
    回复用户的问题。
    """
    answer: str = Field(..., description="回复用户的问题")


class Response(BaseModel):
    response: Joke | CoversationalResponse


async def run():
    llm_with_structured_output = llm.with_structured_output(Response, include_raw=True)

    chain = RunnableParallel(
        {
            "question": RunnablePassthrough(),
            "response": llm_with_structured_output
        } 
    ) | (lambda x: x["response"])

    res = await chain.ainvoke("给我将一个猫的笑话。")
    logger.info(res)

    res = await chain.ainvoke("你叫什么")
    logger.info(res)

    async for i in llm_with_structured_output.astream("给我将一个关于猩猩的笑话。"):
        logger.info(i)


    llm_with_structured_output = llm.with_structured_output(None, method="json_mode")

    async for i in llm_with_structured_output.astream(
        "给我将一个关于猩猩的笑话。Json 格式。包含setup, punchline两个键"
    ):
        logger.info(i)
