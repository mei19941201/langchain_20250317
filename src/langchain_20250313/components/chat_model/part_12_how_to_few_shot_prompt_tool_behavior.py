from langchain_20250313.core import llm, logger

from langchain_core.tools import tool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import (
    AIMessage, 
    HumanMessage, 
    ToolCall, 
    ToolMessage,
    SystemMessage
)


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

    chat_history = (
        HumanMessage("计算1024加上6148再减去20"),
        AIMessage(
            content="", 
            name="example_assiatant",
            tool_calls=[{"name": "add", "args": {"a": 1024, "b": 6148}, "id": "1"}]
        ),
        ToolMessage(content="7072", tool_call_id="1"),

        AIMessage(
            content="", 
            name="example_assiatant",
            tool_calls=[{"name": "add", "args": {"a": 7072, "b": -20}, "id": "2"}]
        ),
        ToolMessage(content="7052", tool_call_id="2"),

        AIMessage(
            content="1024加上6148再减去20结果等于7052",
            name="example_assiatant"
        )
    )

    system = """你是一个工具调用专家，你不自己做计算，你很擅长使用工具解决问题。
参照示例一步一步的解决用户问题，保证工具使用的顺序和计算顺序保持一致。
"""
    messages = [
        SystemMessage(system),
        *chat_history,
        HumanMessage("计算119乘以8再减去20")
    ]

    llm.temperature = 0

    tools = [add, multiply]
    TOOLS = {
        i.name: i for i in tools
    }
    llm_with_tool = llm.bind_tools(tools, parallel_tool_calls=False)

    # 终止判断
    man_template = """
你是一个ai会话主管，你可以根据上下文判断用户的问题是否的到解决，只输出True 或者False, 不对结果进行分析。
"""
    msgs = [
        SystemMessage(man_template),
        HumanMessage("计算119乘以8再减去20")
    ]

    while True:
        res = llm_with_tool.invoke(messages)
        messages.append(res)
        msgs.append(res)
        logger.info(res)

        if res.content == "" and "tool_calls" in res.additional_kwargs:
            tool_call = res.tool_calls
            for i in tool_call:
                tool_res = TOOLS[i["name"]].invoke(input=i["args"])
                tool_msg = ToolMessage(content=tool_res, tool_call_id=i["id"])
                logger.info(tool_msg)
                messages.append(tool_msg)
                msgs.append(tool_msg)
        
        if "True" in llm.invoke(msgs).content.split("</think>")[-1]:
            break