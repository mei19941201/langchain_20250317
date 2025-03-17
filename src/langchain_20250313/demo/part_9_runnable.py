from langchain_20250313.core import llm, logger


from langchain_core.tools import tool

@tool
def a(s: str):
    """
    split string to list

    Args:
        s (str): input string
    """
    return list(s)


@tool
def b(l: list[str]):
    """
    join list to string

    Args:
        l (list[str]): input list
    """
    return "_".join(l)
        


def part9():
    chain = a | b
    res = chain.invoke("hello")
    logger.info(res)