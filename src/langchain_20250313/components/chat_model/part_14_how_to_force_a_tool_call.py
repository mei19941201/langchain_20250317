from langchain_20250313.core import llm, logger

from langchain_core.tools import tool


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
    llm_with_tool = llm.bind_tools([add, multiply], tool_choice="multiply")
    res = await llm_with_tool.ainvoke("32加54等于多少")
    logger.info(res)

    llm_with_tool = llm.bind_tools([add, multiply], tool_choice="any")
    res = await llm_with_tool.ainvoke("你好，你叫什么")
    logger.info(res)