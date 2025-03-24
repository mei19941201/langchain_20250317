from langchain_20250313.core import llm, embedding, logger, loop

import json
import torch
import numpy as np
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from transformers import AutoModel, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("name")
model = AutoTokenizer.from_pretrained("name")

# rerank
async def call_rerank(query: str, docs: list[Document], top_n: int = 3):
        """
        Re-ranks a list of documents based on their relevance to a given query.

        Args:
            query (str): The query string to compare against the documents.
            docs (list[Document]): A list of Document objects to be re-ranked.
            top_n (int, optional): The number of top documents to return. Defaults to 3.
        Returns:
            list[Document]: A list of the top_n most relevant Document objects.
        
        """    
        pairs = [[query, i.page_content] for i in docs]
        with torch.no_grad():
            inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt')
            scores = model(**inputs, return_dict=True).logits.view(-1, ).float().cpu().numpy()
        sorted_index = np.argsort(scores)[::-1]
        sorted_index = sorted_index[:min(len(sorted_index), top_n)]
        return [docs[i] for i in sorted_index]


class MultiQuery(BaseModel):
    """
    提取多查询生成的多个问题。
    """
    questions: list[str] = Field(..., description="多查询生成的问题")



async def multi_query(question: str, num_question: int = 3):
    template = """
You are an AI language model assistant. Your task is to generate {num_question} 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}
"""

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm.with_structured_output(MultiQuery)

    res: MultiQuery = await chain.ainvoke({"question": question, "num_question": num_question})

    logger.info(type(res))
    logger.info(res)
    for i in res.questions:
        yield i


async def rag_fusion(question: str, retriever: VectorStoreRetriever, top_n: int = 3):
    # rag 混合

    query_docs = {}
    async for i in multi_query(question=question):
        docs = await retriever.ainvoke(input=i)
        for j in docs:
            tool_name = j.metadata["tool_name"]
            if tool_name not in query_docs:
                query_docs[j.metadata["tool_name"]] = j
        logger.info(i)
        logger.info([i.metadata["tool_name"] for i in docs])
    logger.info(len(query_docs))
    for idx, i in enumerate(query_docs.values()):
        logger.info(f"\n{idx}: {i.metadata['tool_name']}")

    reranked_docs = await call_rerank(question, list(query_docs.values()), top_n=top_n)

    for idx, i in enumerate(reranked_docs):
        logger.info(f"\n{idx}: {i.metadata['tool_name']}")
    return reranked_docs


def test():
    
    question = "请帮我导出要货机构为【杜智勇 19181738589】，日期区间为2月1日到2月28日之间的所有配送申请单"
    
    with open("./tools.json", "r", encoding="utf8")as f:
        tools = json.load(f)

    tool_docs = [
        Document(
            page_content=i["tool_head"], metadata={"tool_name": i["tool_name"]} 
        ) for i in tools
    ]
    tool_db = Chroma(
        collection_name="tool_db",
        embedding_function= embedding
    )
    tool_db.add_documents(tool_docs)
    tool_retriever = tool_db.as_retriever()


    loop.run_until_complete(rag_fusion(question, tool_retriever))