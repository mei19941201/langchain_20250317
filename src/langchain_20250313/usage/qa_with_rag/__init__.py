from langchain_20250313.core import loop
from .part_1_how_to_add_chat_history import run


def qa_with_rag():
    loop.run_until_complete(run())