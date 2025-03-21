from langchain_20250313.core import llm, logger

from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.outputs import GenerationChunk


async def run():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI助手。"),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}。现在的时间是：{t}")
    ])

    prompt = prompt.partial(t=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    res = await prompt.ainvoke({"question": "你好", "chat_history": []})
    logger.info(res)