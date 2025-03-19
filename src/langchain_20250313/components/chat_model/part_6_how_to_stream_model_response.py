from langchain_20250313.core import llm, logger

from time import sleep
from pydantic import BaseModel, Field
from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("Qwen/QwQ-32B")


async def run():
    chunks = []
    async for i in llm.astream("你好，我叫victor"):
        chunks.append(i.content)

    logger.info(chunks)

    token = tokenizer.encode("".join(chunks))
    token = tokenizer.batch_decode(token)
    logger.info(token)