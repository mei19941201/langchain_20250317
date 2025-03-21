from langchain_20250313.core import llm, logger, embedding

from langchain_chroma import Chroma
from langchain_core.prompts import (
    PromptTemplate, 
    ChatPromptTemplate,
    FewShotPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.runnables import RunnablePassthrough


examples = [
    {
        "question": "请帮我导出要货机构为【杜智勇 19181738589】，日期区间为2月1日到2月28日之间的所有配送申请单",
        "answer": "export_delivery_request_form"
    },
    {
        "question": "请帮我导出3月1日到3月8日期间，所有待付款的配送申请单",
        "answer": "export_the_pending_shipping_request_form"
    }
]


async def run():
    template = PromptTemplate.from_template(
        """\nQuestion:{question}\n{answer}"""
    )

    res = await template.ainvoke(examples[0])
    logger.info(res.to_string())

    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=template,
        suffix="Question: {input}",
        input_variables=["input"],
    )

    res = await few_shot_template.ainvoke({"input": "查询2025年2月整个月的杜勇的配送申请单"})
    logger.info(res.to_string())


async def run():
    selector = SemanticSimilarityExampleSelector.from_examples(
        examples=examples,
        embeddings=embedding,
        vectorstore_cls=Chroma,
        k=1
    )

    q = "查询2025年2月整个月的杜勇的配送申请单"

    res = selector.select_examples({"question": q})
    # logger.info(res)

    example_template = ChatPromptTemplate.from_messages(
        [
            ("human","{question}"),
            ("ai", "{answer}")
        ]
    )

    temp = FewShotChatMessagePromptTemplate(
        example_selector=selector,
        example_prompt=example_template,
    )

    res = await temp.ainvoke({"question": q})
    # logger.info(res)

    template = ChatPromptTemplate.from_messages([
        ("system","你是一个AI助手。"),
        temp,
        ("human", "{question}")
    ])

    chain = template
    # 获取相似的example,装填到模板中
    # chain = {
    #     "question": RunnablePassthrough(),
    #     "example": lambda x: temp.invoke({"question": x}).to_messages()
    # } | template

    res = await chain.ainvoke({"question": q})
    for i in res.to_messages():
        logger.info(i)