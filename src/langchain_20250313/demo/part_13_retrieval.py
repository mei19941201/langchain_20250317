from langchain_20250313.core import llm, logger, embedding, loop, call_rerank as c_rerank

import json
import numpy as np
from functools import partial
from pydantic import BaseModel, Field

from langchain_chroma import Chroma

from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.vectorstores import VectorStoreRetriever

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank


# 查询分析
# 查询结构化
# 重排


class MultiQuery(BaseModel):
    "提取生成的三个问题"
    queries: list[str] = Field(..., description="三个不同的问题")


async def init_retireval(top_k: int = 1):

    with open("./tools.json", "r", encoding="utf8")as f:
        tools = json.load(f)

    docs = [
        Document(
            page_content=i["tool_head"],
            metadata={
                "tool_name": i["tool_name"],
            }
        ) for i in tools
    ]

    tool_db = Chroma(
        collection_name="tool_db",
        embedding_function=embedding
    )

    tool_db.add_documents(docs)

    retrievar = tool_db.as_retriever(search_kwargs={"k": top_k})

    return retrievar


async def load_instruct():
    with open("./testset.json", "r", encoding="utf8")as f:
        instructs = json.load(f)
    for i in instructs:
        yield i


async def query_analysis():
    
    template="""You are an AI language model assistant. Your task is 
    to generate 3 different versions of the given user 
    question to retrieve relevant documents from a vector database. 
    By generating multiple perspectives on the user question, 
    your goal is to help the user overcome some of the limitations 
    of distance-based similarity search. Provide these alternative 
    questions separated by newlines. Original question: {question}"""
    template = ChatPromptTemplate.from_template(
        template
    )

    llm_ = llm.with_structured_output(MultiQuery)
    chain = template | llm_

    async for i in load_instruct():
        question = i["question"]
        mq: MultiQuery = await chain.ainvoke({"question": question})
        for j in mq.queries:
            yield j, i["answer"]


class ReRank:
    def __init__(self, retriever, top_n):
        self.retriever = retriever
        self.top_n = top_n
    
    async def ainvoke(self, question: str) ->list[Document]:
        """
        Rerank

        Args:
            question: 用户查询
            retriever: 检索器

        """
        dosc = await self.retriever.ainvoke(question)
        pairs = [[question, i.page_content] for i in dosc]
        score = await c_rerank(pairs)
        sort_ = np.argsort(score)[::-1][:self.top_n]
        docs_ = [dosc[i] for i in sort_]    
        return docs_


async def metric(top_k: int = 5, top_n: int = 3, rerank: bool = False):
    total = 0
    correct_top1 = 0
    correct_topn = 0
    retirever = await init_retireval(top_k=top_k)
    if rerank:
        retirever = ReRank(retirever, top_n=top_n)

    async for q, a in query_analysis():
        total += 1
        search_ok = False
        l = logger.error

        res = await retirever.ainvoke(q)

        for idx, i in enumerate(res):
            if i.metadata["tool_name"] == a:
                correct_topn += 1
                search_ok = True
                if idx == 0:
                    correct_top1 += 1
                break
        if search_ok:
            l = logger.info
        l(f"NO.{str(total):5} {q}")
        l(f"NO.{str(total):5} {a}\n")
        if not search_ok:
            for idx, i in enumerate(res):
                l(f"\nNO.{str(idx):5}\n" + i.page_content)

    logger.info(f"\ntop1: {round(correct_top1 / total * 100, 1)}%.\ntop{top_k}: {round(correct_topn / total * 100, 1)}%.")


def part13():
    loop.run_until_complete(metric(rerank=True))