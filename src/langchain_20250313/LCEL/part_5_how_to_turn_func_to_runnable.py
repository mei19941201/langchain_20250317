from langchain_20250313.core import llm, logger

from typing import Iterator, Generator
from langchain_core.messages import BaseMessageChunk


def parse(msgs: Iterator[BaseMessageChunk]):
    for i in msgs:
        yield i.content


async def run():
    
    chain = llm | parse

    # for i in chain.stream("你好"):
    #     print(i, end="")

    res = chain.invoke("你好")
    logger.info(res)