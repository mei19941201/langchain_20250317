from langchain_20250313.core import llm, logger

from typing import overload, Iterator, Iterable, AsyncIterator
from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage, BaseMessageChunk
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser, BaseTransformOutputParser
from langchain_core.outputs import GenerationChunk


async def test(input: AsyncIterator[BaseMessageChunk]):
    NOT_THINK = False
    async for i in input:
        if "</think>" in i.content:
            NOT_THINK = True
            continue

        if NOT_THINK:
            yield i.content


async def run():

    prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话，字数不超过100。")

    chain = prompt | llm | test

    async for i in chain.astream("猫咪"):
        print(i, end="")

