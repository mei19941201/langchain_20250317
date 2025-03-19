from langchain_20250313.core import llm, logger

from pydantic import BaseModel, Field


async def run():
    llm_with_prob = llm.bind(logprobs=True)
    res = await llm_with_prob.ainvoke("你好，我是victor")
    logger.info(res)
    logger.info(res.response_metadata)
