from langchain_20250313.core import llm, logger

from typing import TypedDict, Annotated
from langchain_core.messages import (
    AnyMessage, 
    AIMessage,
    HumanMessage
)
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages


def add(left, right):
    return left + right

class State(TypedDict):
    """
    状态就是整个图中需要传递的东西, 每个节点的返回和结果的返回也必须是状态。
    每个状态字段可以有一个reducer函数用来告诉如何更新状态。
    """
    messages: Annotated[list[AnyMessage], add_messages]
    extra_field: int


# MessagesState 封装了基础的messages, 确保了聊天记录。自建的状态最好直接继承这个类
class State2(MessagesState):
    extra_field: int


# 节点，接受一个状态，输出一个状态，输出的状态的每个字段根据相应的reducer函数进行更新。
def node(state: State2):
    new_msg = AIMessage("Hello")
    return {
        "messages": new_msg,
    }


async def run():
    graph_builder = StateGraph(State2)
    graph_builder.add_node(node)
    graph_builder.add_edge(START, "node")
    graph_builder.add_edge("node", END)
    graph = graph_builder.compile()

    logger.info("\n" + graph.get_graph().draw_ascii())

    res = graph.invoke({"messages": [HumanMessage("Hi")]})
    logger.info(res)

    for i in res["messages"]:
        i.pretty_print()