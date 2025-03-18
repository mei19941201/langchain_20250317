from langchain_20250313.core import llm, logger

import json
from datetime import datetime
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, ToolCall
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


@tool(parse_docstring=True)
def get_datetime():
    """
    获取当前的日期和时间
    """
    return datetime.now()


@tool(parse_docstring=True)
def welcome(user: str):
    """
    回答用户的问好。

    Args:
        user: 用户姓名
    """
    return f"{user} welcome"


async def run():
    logger.info(f"{__file__} run")
    tools = [get_datetime, welcome]
    TOOLS = {
        i.name: i for i in tools
    }
    llm_with_tool = llm.bind_tools(tools)
    msgs = [HumanMessage("你好，我是陈近南。现在几点了")]

    i = await llm_with_tool.ainvoke(
        msgs
    )
    msgs.append(i)
    logger.info(i)
    if i.content == "" and "tool_calls" in i.additional_kwargs:
        tool_call = i.tool_calls
        for j in tool_call:
            call = ToolCall(name=j["name"], args=j["args"], id=j["id"])
            # msgs.append(call)
            logger.info(call)
            tool_res = TOOLS[j["name"]].invoke(input=j["args"])
            msg = ToolMessage(content=tool_res, tool_call_id=j["id"], name=j["name"])
            msgs.append(msg)
            logger.info(msg)
    res = await llm_with_tool.ainvoke(msgs)
    logger.info(res)
    logger.info(f"{__file__} done")