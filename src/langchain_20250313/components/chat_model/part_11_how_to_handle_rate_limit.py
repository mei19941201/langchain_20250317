from langchain_20250313.core import llm, logger

from time import time
from langchain_core.rate_limiters import InMemoryRateLimiter


async def run():
    llm.rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1
    )

    for i in range(5):
        t1 = time()
        res = await llm.ainvoke("你好。")
        logger.info(res)
        t2 = time()
        logger.info(f"runtime: {round(t2 - t1)}s")