from langchain_20250313.core import loop

from .part_1_chat_bot import run


def graph_base():
    loop.run_until_complete(run())