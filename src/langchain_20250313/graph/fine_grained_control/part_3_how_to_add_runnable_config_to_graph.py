from langchain_20250313.core import llm, logger

from typing import AsyncIterator
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, trim_messages, HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver


class State(MessagesState):
    ...

class Config(BaseModel):
    system_message: SystemMessage | None


trim = trim_messages(
    token_counter=len,
    max_tokens=10,
    include_system=True,
    start_on=["human"],
    end_on=["human", "tool"],
)


async def llm_run(state: State, config: RunnableConfig):
    msgs = state["messages"]
    # add system messages
    system_message = config["configurable"].get("system_message", [])
    msgs = system_message + msgs
    # trim messages
    trimed_msgs = await trim.ainvoke(msgs)
    for i in trimed_msgs:
        logger.debug(i)
    # call llm
    res = await llm.ainvoke(trimed_msgs)
    # update messages
    return {
        "messages": [res]
    }



async def run():
    builder = StateGraph(State, Config)
    builder.add_node(llm_run)
    builder.add_edge(START, "llm_run")
    builder.add_edge("llm_run", END)
    graph = builder.compile(checkpointer=InMemorySaver())

    while True:
        i = input("input: ")
        x = i.split("|")
        if len(x) == 2:
            s, q = x
            s = [SystemMessage(s)]
            q = [HumanMessage(q)]
        else:
            s = []
            q = [HumanMessage(i)]
        if q[0].content == "q":
            break
        logger.info(i)
        res = await graph.ainvoke({"messages": q}, {"configurable": {"system_message": s, "thread_id": 1}})
        logger.info(res["messages"][-1])
