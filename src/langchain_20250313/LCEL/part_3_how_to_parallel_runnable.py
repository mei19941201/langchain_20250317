from langchain_20250313.core import llm, logger, embedding

from functools import partial
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever

async def build_retriever():
    docs = [
        Document("陈近南是清朝年间的民间反抗组织首领"),
        Document("韦小宝是陈近南的徒弟"),
        Document("天体会总舵主是韦小宝的师傅")
    ]

    db = Chroma(embedding_function=embedding)
    db.add_documents(docs)
    retriever: VectorStoreRetriever = db.as_retriever()
    return retriever


@chain
async def retriever_with_log(question: str, config):
    logger.info(config)
    retriever = config["configurable"]["retriever"]
    docs: list[Document] = await retriever.ainvoke(question)
    out = ""
    for idx, i in enumerate(docs):
        logger.info(i)
        out += f"NO.{idx} {i.page_content}\n"
    return out


async def parse_retriever(docs: list[Document]):
    out = ""
    for idx, i in enumerate(docs):
        logger.info(i)
        out += f"NO.{idx} {i.page_content}\n"
    return out


async def run():
    retriever = await build_retriever()

    retriever_chain = retriever | parse_retriever

    rag_prompt = """根据Content中的内容回答用户问题：

Content:
{content}

Question:
{question}

Answer:"""

    rag_prompt = ChatPromptTemplate.from_template(rag_prompt)

    chain = {
        "content": retriever_chain,
        "question": RunnablePassthrough(),
    } | rag_prompt | llm | StrOutputParser()

    out = ""
    async for i in chain.astream("陈近南是谁？", config={"configurable": {"retriever": retriever}}):
        out += i
        print(i, end="")