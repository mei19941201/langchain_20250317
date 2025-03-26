from langchain_20250313.core import llm, logger

from typing import AsyncIterator
from langchain_core.messages import BaseMessage, trim_messages, BaseMessageChunk, HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, chain, RunnableParallel
from langchain_core.output_parsers import StrOutputParser


STROE = {}


async def get_history(question: str, config: dict):
    id = config["configurable"]["thread_id"]
    if id not in STROE:
        STROE[id] = InMemoryChatMessageHistory()
    chat_his: InMemoryChatMessageHistory = STROE.get(id)
    his = await chat_his.aget_messages()
    await chat_his.aadd_messages([HumanMessage(question)])
    return his


async def add_history(msgs: AsyncIterator[BaseMessageChunk], config: dict):
    id = config["configurable"]["thread_id"]
    chat_his: InMemoryChatMessageHistory = STROE.get(id, InMemoryChatMessageHistory())
    msg = None
    async for i in msgs:
        if msg is None:
            msg = i
        else:
            msg += i
        yield i
    yield "\n"

    await chat_his.aadd_messages([msg])

async def log_history(info: dict):
    logger.info(info["question"])
    for i in info["chat_history"]:
        logger.debug(i)
    logger.debug("")
    return info


async def run():
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI助手。"),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])

    trim = trim_messages(
        token_counter=len,
        max_tokens=10,
        include_system=True,
        start_on=["human"],
        end_on=["human", "tool"]
    )


    input_ = RunnableParallel({
        "question": RunnablePassthrough(),
        "chat_history": get_history
    }) | log_history | prompt | trim | llm | add_history | StrOutputParser()

    while True:
        x = input("input: ")
        if x == "q":
            break
        async for i in input_.astream(x, config={"configurable": {"thread_id": 1}}):
            print(i, end="")