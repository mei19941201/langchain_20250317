from langchain_20250313.core import llm, logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


async def run():
    llm.temperature
    prompt = ChatPromptTemplate.from_messages([
        ("system", "根据用户输入，使用数学符号对其进行表示放入QUESTION中，解答数学问题，将解答步骤放入SOLUTION，格式为：\nQUESTION:...\nSOLUTION:..."),
        ("human", "{math}")
    ])

    chain = prompt | llm.bind(stop="SOLUTION") | StrOutputParser()

    res = await chain.ainvoke("x的三次方加上7等于12")
    logger.info(res)