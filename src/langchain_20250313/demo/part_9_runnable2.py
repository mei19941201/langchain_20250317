from operator import itemgetter
from langchain_20250313.core import llm, logger, loop

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser


def branch():
    p_template = """
you are an ai physisist, and you can help use to solve the following physics problem:
{question}
"""
    physics = ChatPromptTemplate.from_template(p_template)
    p_chain = physics | llm | StrOutputParser()

    m_template = """
you are an ai mathematician, and you can help use to solve the following math problem:
{question}
"""
    math = ChatPromptTemplate.from_template(m_template)
    m_chain = math | llm | StrOutputParser()

    o_template = """
you are a helpfun ai assistant, and you can help use to solve the following problem:
{question}
"""
    other = ChatPromptTemplate.from_template(o_template)
    o_chain = other | llm | StrOutputParser()

    c_template = """
根据问题描述，对问题进行分类：physics, math, other, 只返回一个分类，具体问题如下：
{question}

分类结果：
"""
    classify = ChatPromptTemplate.from_template(c_template)
    c_chain = classify | llm | StrOutputParser()

    branch_chain = RunnableBranch(
        (lambda x: "physics" in x["topic"], p_chain),
        (lambda x: "math" in x["topic"], m_chain),
        o_chain
    )

    chain = {
        "topic": c_chain,
        "question": itemgetter("question")
    } | branch_chain


    res = chain.invoke({
        # "question": "白炽灯灯丝烧断后再搭上，点燃时更亮，这是为什么?",
        "question": "先化简，再求值：(x+1)²-(x-2)(2+x)，其中x=3",
        # "question": "a physics problem",
    })

    logger.info(res)




def part9_2():
    logger.info("part9_2 running")
    branch()

    logger.info("part9_2 done")