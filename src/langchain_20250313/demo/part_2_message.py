import json
from langchain_20250313.core import llm, logger
from uuid import uuid1

from langchain_core.messages import (
    BaseMessage, 
    ChatMessage, 
    SystemMessage,
    AIMessage,
    HumanMessage, 
    ToolMessage,
    FunctionMessage,

    BaseMessageChunk,
    SystemMessageChunk,
    AIMessageChunk,
    HumanMessageChunk,
    ToolMessageChunk,
    FunctionMessageChunk,

    ToolCall,
    ToolCallChunk,
)
from langchain_core.tools import tool

from datetime import datetime


@tool
def get_datetime():
    """
    获取当前日期和时间
    """
    return datetime.now()



def part2():
    # res = llm.invoke([
    #     SystemMessage(content="你是一位天外来客，你刚刚来到这里。"),
    #     HumanMessage(content="你好，我的朋友。"),
    #     ]
    # )
    # logger.info(res.content)

    msgs = [
        SystemMessage("你是一位天外来客，你刚刚来到地球。"),
        HumanMessage("你好，我的朋友。现在是几点了。"),
    ]

    llm_ = llm.bind_tools([get_datetime])

    res = llm_.invoke(msgs)
    logger.info(res)
    content = res.content
    additional_kwargs = res.additional_kwargs
    if content == "" and "tool_calls" in additional_kwargs:
        for i in additional_kwargs["tool_calls"]:
            function = i["function"]
            tool_name = function["name"]
            tool_args = json.loads(function["arguments"])
            call_id = str(uuid1())
            res = eval(tool_name).invoke(input=tool_args)
            msg = ToolMessage(content=str(res), tool_call_id=call_id)
            logger.info(msg)
            msgs.append(msg)
            
    res = llm_.invoke(msgs)
    logger.info(res)