from langchain_20250313.core import llm, logger, graph_show

from operator import add
from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Send


class Topics(BaseModel):
    data: list[str] = Field(..., description="生成的多个话题。")


class Joke(BaseModel):
    content: str = Field(..., description="根据主题生成的笑话内容。")


class State(MessagesState):
    topic: str
    topics: list[str]
    jokes: Annotated[list[str], add]
    best_joke: str


class JokeState(MessagesState):
    topic: str


gen_topic_parser = PydanticOutputParser(pydantic_object=Topics)


gen_topic_prompt = """
根据下面Topic中的话题生成3个相同类型的话题。
按照如下格式进行返回:
{fmt}
Topic: 
{topic}
Three_same_topic:"""
gen_topic_prompt = ChatPromptTemplate.from_template(
    gen_topic_prompt
    ).partial(fmt=Topics.model_json_schema())


async def gen_topic_node(state: State):
    chain = gen_topic_prompt | llm | gen_topic_parser
    topic: Topics = await chain.ainvoke(state["topic"])
    return {
        "topics": topic.data
    }


gen_joke_parser = PydanticOutputParser(pydantic_object=Joke)


gen_joke_prompt = """
根据下面Topic中的话题生成1个笑话。
按照如下格式进行返回:
{fmt}
Topic: 
{topic}
Joke:"""
gen_joke_prompt = ChatPromptTemplate.from_template(
    gen_joke_prompt
    ).partial(fmt=Joke.model_json_schema())


async def gen_joke_node(state: JokeState):
    chain = gen_joke_prompt | llm | gen_joke_parser
    joke: Joke = await chain.ainvoke(state["topic"])
    return {"jokes": [joke.content]}


async def map_reduce_branch(state: State):
    return [Send("gen_joke_node", {"topic": i}) for i in state["topics"]]


async def run():
    
    builder = StateGraph(State)
    builder.add_node(gen_topic_node)
    builder.add_node(gen_joke_node)
    builder.add_edge(START, "gen_topic_node")
    builder.add_conditional_edges(
        "gen_topic_node",
        map_reduce_branch
    )

    graph = builder.compile()

    res = await graph.ainvoke({"topic": "猫咪"})
    logger.info(res)