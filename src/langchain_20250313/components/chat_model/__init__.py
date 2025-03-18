from langchain_20250313.core import loop

from .part_1_how_to_use_tool import run


def chat_model():
    loop.run_until_complete(run())