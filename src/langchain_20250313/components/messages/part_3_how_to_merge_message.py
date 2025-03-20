from langchain_20250313.core import llm, logger

from langchain_core.messages import (
    merge_message_runs
)
from langchain_core.prompts import ChatPromptTemplate

# 这个功能的一大好处就是方便调试系统提示词

async def run():
    merge = merge_message_runs()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个ai助手"),
        ("system", "你擅长解决用户的问题"),
        ("human", "{question}"),
    ])

    chain = prompt | merge

    res = await chain.ainvoke({"question": "你能做什么"})
    logger.info(res)