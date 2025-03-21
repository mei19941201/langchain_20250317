from typing import AsyncIterator
from langchain_20250313.core import llm, logger

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    AIMessageChunk,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk
from langchain_core.tools import tool

async def run():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个AI助手。"),
            ("human", "{question}"),
        ]
    )

    async def parse_msg(msg: list[AIMessage, AIMessageChunk]):
        """
        解析消息
        """
        if isinstance(msg, AIMessage):
            yield msg.content
        else:
            async for i in msg:
                logger.info(type(i))
                logger.info(i)
                yield i.content


    # parse_msg这玩意儿需要实现invoke, stream的同步和异步才OK
    chain1 = prompt | llm | parse_msg

    # async for i in chain1.astream(
    #     "你好，我是陈近南。"
    # ):
    #     print(i, end="")

    # res = await chain1.ainvoke("你好，我是陈近南。")
    # logger.info(res)

    chain2 = prompt | llm | StrOutputParser()
    async for i in chain2.astream(
        "你好，我是陈近南。"
    ):
        logger.info(i)
        print(i, end="")