from langchain_20250313.core import llm, logger

from functools import partial
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    trim_messages,
    BaseMessage
)
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory


@tool(parse_docstring=True)
def multiply(a: int, b: int):
    """
    计算两个数的乘积。

    Args:
        a: 第一个数
        b: 第二个数
    """
    return a * b


@tool(parse_docstring=True)
def add(a: int, b: int):
    """
    计算两个数的和。

    Args:
        a: 第一个数
        b: 第二个数
    """
    return a + b


async def run():
    # 记忆实现
    history = []
    # 聊天模板
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage("你是一个ai助手,帮助用户解决问题。"),
            MessagesPlaceholder("history"),
            ("human", "{question}")
        ]
    )

    # 消息整理
    trim = partial(
        trim_messages,
        token_counter=len,
        max_tokens=8,
        strategy="last",
        start_on="human",
        end_on=["human", "tool"],
        include_system=True
    )

    llm_with_tool = llm.bind_tools([add, multiply])
    chain = template | llm_with_tool

    while True:
        i = input("input: ")
        if i == "q":
            break

        history.append(HumanMessage(i))
        if len(history) > 1:
            history_ = trim(messages=history)
        else:
            history_ = []

        for i in history_:
            logger.info(i)
        res = await chain.ainvoke({"question": i, "history": history_})
        print(res.content if res.content != "" else res.tool_calls)
        history.append(res)

        for j in res.tool_calls:
            tool_res = eval(j["name"]).invoke(j["args"])
            print(tool_res)
            history.append(ToolMessage(tool_res, tool_call_id=j["id"]))
        
        for i in history:
            logger.debug(i)


async def run1():
    history = [
        SystemMessage("你是一个ai助手,帮助用户解决问题。")
    ]

    trim = trim_messages(
        token_counter=len,
        max_tokens=8,
        strategy="last",
        start_on="human",
        end_on=["human", "tool"],
        include_system=True
    )

    def user_input(s: str):
        history.append(HumanMessage(s))
        for i in history:
            logger.debug(i)
        trim_history = trim.invoke(history)
        for i in trim_history:
            logger.info(i)
        return trim_history
    
    llm_with_tool = llm.bind_tools([add, multiply])

    def save_llm_response(msg: BaseMessage):
        history.append(msg)
        print(msg.content if msg.content != "" else msg.tool_calls)
        for j in msg.tool_calls:
            tool_res = eval(j["name"]).invoke(j["args"])
            print(tool_res)
            history.append(ToolMessage(tool_res, tool_call_id=j["id"]))

    chain = user_input | llm_with_tool | save_llm_response

    while True:
        i = input("input: ")
        if i == "q":
            break
        await chain.ainvoke(i)
