from langchain_20250313.core import llm, logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain, RunnablePassthrough, RunnableLambda


async def run():
    math_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI数学家，你擅长解决用户提出的数学问题"),
        ("human", "{question}")
    ])

    physics_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI物理学家，你擅长解决用户提出的物理问题"),
        ("human", "{question}")
    ])

    topic_prompt = ChatPromptTemplate.from_template(
        """根据下列问题，对问题进行分类：math, physics, other。
只输出一个分类，不要输出分析过程。
Question:
{question}
Answer:"""
    )

    topic_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI话题分类专员,根据用户问题，对问题进行分类：math, physics, other。只需要回答分类结果。"),
        ("human", "{question}")
    ])

    async def parse(msg: AIMessage):
        return msg.content.split("</think>")[-1]

    math_chain = math_prompt | llm | StrOutputParser()
    physics_chain = physics_prompt | llm | StrOutputParser()
    topic_chain = topic_prompt | llm | parse
    
    async def router(info: dict):
        logger.info(info)
        if "math" in info["topic"]:
            return math_chain
        elif "physics" in info["topic"]:
            return physics_chain
        else:
            return (lambda x: x["question"]) | llm | StrOutputParser()

    chain_ = {
        "question": RunnablePassthrough(),
        "topic": topic_chain
    } | RunnableLambda(router)

    # q1 = "已知圆的半径为12, 计算圆的周长和面积。"
    # q2 = "光在不同的介质中传播的速度不相同，这个说法正确吗？"
    # q3 = "陈近南是历史上真实存在的人物吗？"

    # for q in [q1, q2, q3]:
    #     async for i in chain_.astream(q):
    #         print(i, end="")


    chain_.get_graph().print_ascii()