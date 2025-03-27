from langchain_20250313.core import llm, logger, graph_show


from typing import Annotated
from operator import add
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command


class State(MessagesState):
    content: Annotated[str, add] = ""
    next: str
    sub: bool = False


async def a(state: State):
    if state["next"] == "b":
        goto = "b"
    else:
        goto = "c"
    
    return Command(
        update={"content": "a"},
        goto=goto,
        graph=Command.PARENT if state["sub"] else None
    )


async def b(state: State):
    return {"content": "b"}


async def c(state: State):
    return {"content": "c"}


async def run():
    builder = StateGraph(State)
    builder.add_edge(START, "a")
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)

    graph = builder.compile()
    # graph_show(graph)
    logger.info("\n" + graph.get_graph().draw_ascii())

    res = await graph.ainvoke({"next": "b"})
    logger.info(res)


async def run2():
    sub_graph = StateGraph(State).add_edge(START, "a").add_node(a).compile()
    
    builder = StateGraph(State)
    builder.add_node("sub_graph", sub_graph)
    builder.add_edge(START, "sub_graph")

    builder.add_node(b)
    builder.add_node(c)

    graph = builder.compile()

    logger.info("\n" + graph.get_graph().draw_ascii())

    res = await graph.ainvoke({"next": "c", "sub": True})
    logger.info(res)