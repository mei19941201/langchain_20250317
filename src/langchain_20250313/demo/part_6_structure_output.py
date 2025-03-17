from langchain_20250313.core import llm, logger

from pydantic import BaseModel, Field


class User(BaseModel):
    """
    提取用户信息
    """
    name: str = Field(description="名字")
    age: int = Field(description="年龄")


def part6():
    llm_ = llm.with_structured_output(User.model_json_schema())
    res = llm_.invoke("你好，我是天地会总舵主陈近南，我今年42岁。")
    logger.info(res)