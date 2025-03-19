from langchain_20250313.core import llm, logger, loop


from langchain_core.tools import tool
from langchain_core.runnables import RunnableParallel

@tool
def a(s: str):
    """
    split string to list

    Args:
        s (str): input string
    """
    return {
        "l": list(s)
    }


@tool
def b(l: list[str]):
    
    """
    join list to string
    """
    return "-".join(l)

@tool
def c(s: str):
    """
    """
    return "-".join(s)


@tool
def d(s: str):
    """
    """
    return "*".join(s)

@tool
def e(s1: str, s2: str):
    """
    """
    return [s1, s2]


def f(s: str):
    return {
        "input": "victor"
    }

@tool
def g(input: str):
    """
    return input
    """
    return input


async def runnable_seq():
    prompt = "admin"
    res1 = await a.ainvoke(prompt)
    logger.info(res1)

    res2 = await b.ainvoke(res1)
    logger.info(res2)

    chain = a | b
    res3 = await chain.ainvoke(prompt)
    logger.info(res3)


async def runnable_parallel():
    prompt = "victor"
    s_ = {
        "s1": c,
        "s2": d
    }
    chain = s_ | e

    res = await chain.ainvoke(prompt)
    logger.info(res)


async def runnable_lambda():
    chain = f | g
    res = await chain.ainvoke("hello")
    logger.info(res)


def part9():
    
    # loop.run_until_complete(runnable_seq())
    loop.run_until_complete(runnable_lambda())