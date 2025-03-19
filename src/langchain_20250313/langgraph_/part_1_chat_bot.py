from langchain_20250313.core import llm, loop, logger

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, Messages




class MyState(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def log_state(state: MyState | dict):
    logger.info(state)
    return state


def chatbot(state: MyState):
    
    return {
        "messages": [
            llm.invoke(state["messages"])
        ]
    }


async def chat_bot():
    logger.info("Starting chat_bot")
    graph = StateGraph(MyState)
    graph.add_node("log_state1", log_state)
    graph.add_edge(START, "log_state1")

    graph.add_node("chatbot", chatbot)
    graph.add_edge("log_state1", "chatbot")

    graph.add_node("log_state2", log_state)
    graph.add_edge("chatbot", "log_state2")

    graph.add_edge("log_state2", END)
    graph = graph.compile()
    while True:
        i = input("Enter a message: ")
        if i == "q":
            break
        res = await graph.ainvoke(
            {"messages": [{"role": "user", "content": i}]}
        )
        logger.info(res)
    logger.info("chat_bot Done")


def lg_part1():
    loop.run_until_complete(chat_bot())
