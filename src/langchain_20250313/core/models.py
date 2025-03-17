import os
import numpy as np
import torch
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from .log import logger


a = load_dotenv()

if a:
    logger.info("env init ok.")

llm = ChatOpenAI(
    model=os.environ["CHAT_MODEL"],
    api_key=os.environ["CHAT_API_KEY"],
    base_url=os.environ["CHAT_BASE_URL"],
)

rerank = OllamaEmbeddings(
    model=os.environ["RERANK_MODEL"],
    base_url=os.environ["RERANK_BASE_URL"]
)

embedding = DashScopeEmbeddings(
    model=os.environ["EMBED_MODEL"],
    dashscope_api_key=os.environ["EMBED_API_KEY"],
)

tokenizer = AutoTokenizer.from_pretrained('./models/bge-reranker-v2-m3', use_fp16=True)
model = AutoModelForSequenceClassification.from_pretrained('./models/bge-reranker-v2-m3')
model.eval()


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
