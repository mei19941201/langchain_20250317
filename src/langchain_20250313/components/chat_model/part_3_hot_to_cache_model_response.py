from langchain_20250313.core import llm, logger

from time import time
from pydantic import BaseModel, Field
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache


async def run():

    # set_llm_cache(InMemoryCache())

    instructions = "你叫什么？"

    for i in range(2):
        t1 = time()
        res = await llm.ainvoke(instructions)
        t2 = time()
        logger.info(f"NO.{str(i):5}{round(t2 - t1)}s {res}")

    # set_llm_cache(InMemoryCache())
    set_llm_cache(SQLiteCache())


    for i in range(2):
        t1 = time()
        res = await llm.ainvoke(instructions)
        t2 = time()
        logger.info(f"NO.{str(i):5}{round(t2 - t1)}s {res}")