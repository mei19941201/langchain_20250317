from langchain_20250313.core import llm, logger

import operator
from typing import Annotated
from langgraph.graph import START, StateGraph, MessagesState, END


class State(MessagesState):
    ...
    data: Annotated[list[str], operator.add]
    witch: str


def node_a(state: State):
    logger.info(f"add a to {state['data']}")
    return {'data': ["a"]}


def node_b(state: State):
    logger.info(f"add b to {state['data']}")
    return {'data': ["b"]}


def node_c(state: State):
    logger.info(f"add c to {state['data']}")
    return {'data': ["c"]}


def node_c2(state: State):
    logger.info(f"add c2 to {state['data']}")
    return {'data': ["c2"]}


def node_d(state: State):
    logger.info(f"add d to {state['data']}")
    return {'data': ["d"]}


async def run():
    builder = StateGraph(State)
    builder.add_node(node_a)
    builder.add_node(node_b)
    builder.add_node(node_c)
    builder.add_node(node_c2)
    builder.add_node(node_d)
    builder.add_edge(START, "node_a")

    # 只有这两个分支是并行的
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_a", "node_c")

    builder.add_edge("node_c", "node_c2")
    builder.add_edge(["node_b", "node_c2"], "node_d")

    graph = builder.compile()
    logger.info("\n" + graph.get_graph().draw_ascii())

    res = await graph.ainvoke({'data': []})

    logger.info(res)



def a(state: State):
    logger.info(f"add a to {state['data']}")
    return {'data': ["a"]}


def b(state: State):
    logger.info(f"add b to {state['data']}")
    return {'data': ["b"]}


def c(state: State):
    logger.info(f"add c to {state['data']}")
    return {'data': ["c"]}


def d(state: State):
    logger.info(f"add d to {state['data']}")
    return {'data': ["d"]}


def e(state: State):
    logger.info(f"add e to {state['data']}")
    return {'data': ["e"]}


def bcd(state: State):
    if state["witch"] == "bc":
        return ["b", "c"]
    elif state["witch"] == "cd":
        return ["c", "d"]
    elif state["witch"] == "bd":
        return ["b", "d"]
    else:
        return ["b", "c", "d"]


async def run2():
    builder = StateGraph(State)
    builder.add_node(a)
    builder.add_node(b)
    builder.add_node(c)
    builder.add_node(d)
    builder.add_node(e)
    builder.add_edge(START, "a")

    builder.add_conditional_edges(
        "a",
        bcd,
        ["b", "c", "d"]
    )

    builder.add_edge("b", "e")
    builder.add_edge("c", "e")
    builder.add_edge("d", "e")
    builder.add_edge("e", END)

    graph = builder.compile()

    logger.info("\n" + graph.get_graph().draw_ascii())

    graph.invoke({"data": [], "witch": "bc"})
    graph.invoke({"data": [], "witch": "cd"})
    graph.invoke({"data": [], "witch": "bd"})
    res = graph.invoke({"data": [], "witch": "bcd"})
    print(type(res))