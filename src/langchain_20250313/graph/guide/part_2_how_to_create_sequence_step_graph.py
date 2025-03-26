from langchain_20250313.core import llm, logger

from langgraph.graph import START, END, StateGraph, MessagesState


class State(MessagesState):
    x: str
    y: str


def step1(state: State):
    return {"x": "a"}


def step2(state: State):
    x = state["x"]
    return {"x": f"{x} b"}


def step3(state: State):
    return {"y": "c"}


async def run():
    builder = StateGraph(State)
    builder.add_sequence([step1, step2, step3])
    builder.add_edge(START, "step1")
    graph = builder.compile()
    logger.info("\n" + graph.get_graph().draw_ascii())

    res = await graph.ainvoke({"x": 1})

    logger.info(res)