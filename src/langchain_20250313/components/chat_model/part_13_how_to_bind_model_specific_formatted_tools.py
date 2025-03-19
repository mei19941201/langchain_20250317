from langchain_20250313.core import llm, logger

import json
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



async def run():
    res = multiply.args_schema.model_json_schema()
    logger.info(
        f"\n{json.dumps(res, ensure_ascii=False, indent=4)}"
    )