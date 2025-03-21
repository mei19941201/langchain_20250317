from langchain_20250313.core import llm, logger

from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class Joke(BaseModel):
    content: str = Field(..., description="笑话的内容")
    rate: int| None = Field(None, description="幽默程度打分0~10分。")


async def run():
    llm_ = llm.with_structured_output(Joke)
    # res = await llm_.ainvoke("讲一个简短的关于猩猩的笑话,再根据好笑程度打分")
    # logger.info(type(res))
    # logger.info(res)


# 这种方式看上去是没用的
    # parser = JsonOutputParser(pydantic_object=Joke)
    # chain = llm_ | parser

    # res = await chain.ainvoke("讲一个简短的关于猩猩的笑话,再根据好笑程度打分")
    # logger.info(type(res))
    # logger.info(res)
