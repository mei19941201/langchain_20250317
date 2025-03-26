from langchain_20250313.core import llm, logger, graph_show

import operator
from io import BytesIO
from typing import Annotated
from langgraph.graph import START, END, StateGraph, MessagesState
import numpy as np
import cv2

class State(MessagesState):
    count: Annotated[int, operator.add]


def node_a(state: State):
    logger.info(f"a node add 1 to {state['count']}")
    return {"count": 1}

def node_b(state: State):
    logger.info(f"b node add 1 to {state['count']}")
    return {"count": 1}

def cycle_a(state: State):
    if state["count"] >= 10:
        return END
    return "node_b"


async def run():
    builder = StateGraph(State)
    builder.add_node(node_a)
    builder.add_node(node_b)
    builder.add_edge(START, "node_a")
    builder.add_edge("node_b", "node_a")
    builder.add_conditional_edges(
        "node_a",
        cycle_a,
    )
    graph = builder.compile()

    graph_show(graph)

    res = graph.invoke({"count": 0})
    print(res)



def a(state: State):
    logger.info(f"a node add 1 to {state['count']}")
    return {"count": 1}


def b(state: State):
    logger.info(f"b node add 1 to {state['count']}")
    return {"count": 1}


def c(state: State):
    logger.info(f"c node add 1 to {state['count']}")
    return {"count": 1}


def d(state: State):
    logger.info(f"d node add 1 to {state['count']}")
    return {"count": 1}


def e(state: State):
    logger.info(f"e node add 1 to {state['count']}")
    return {"count": 1}


def cycle_(state: State):
    if state["count"] >= 10:
        return END
    return "b"


async def run2():
    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)
    builder.add_node(d)
    builder.add_edge(START, "a")
    builder.add_conditional_edges(
        "a",
        cycle_,
        ["b", END]
    )
    builder.add_edge("b", "c")
    builder.add_edge("b", "d")
    builder.add_edge(["c", "d"], "a")
    graph = builder.compile()
    graph_show(graph)
    graph.invoke({"count": 0})