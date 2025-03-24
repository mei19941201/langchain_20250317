from langchain_20250313.core import llm, logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

async def run():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI冷笑话大师，你很擅长根据用户的提示生成冷笑话。不需要做任何的分析和讲解。笑话保证在三句话以内。"),
        ("human", "请给我讲一个关于{topic}的笑话")
    ])
    chain = prompt | llm | StrOutputParser() | (lambda x: x.split("</think>")[-1].strip())
    # res = await chain.ainvoke("熊")
    # logger.info(res)

    prompt2 = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI冷笑话评价员，你很擅长对笑话进行1到10分的打分，只输出分数，不要做出任何分析"),
        ("human", "评价一个这个冷笑话。{joke}")
    ])

    chain2 = {
        "joke": chain
    } | prompt2 | llm | StrOutputParser()


    res = await chain2.ainvoke("熊")
    logger.info(res)