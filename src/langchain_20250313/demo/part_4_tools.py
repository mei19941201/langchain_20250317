from datetime import datetime

from langchain_core.tools import tool
from langchain_core.tools import BaseToolkit
from langchain_core.tools.structured import StructuredTool

from langchain_20250313.core import llm, logger


@tool(parse_docstring=True)
def get_datetime():
    """
    获取当前日期和时间。
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool(parse_docstring=True)
def add(a: int, b: int):
    """
    求两个整数的和。

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a + b

def part4():

    logger.info(
        add.args_schema.model_json_schema()
    )

    llm_ = llm.bind_tools([add, get_datetime])
    logger.info(llm_)
    for i in llm_.stream("现在几点了。"):
        print(i.content, end="")