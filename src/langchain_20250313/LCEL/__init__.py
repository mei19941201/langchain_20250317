from langchain_20250313.core import loop

from .part_1_how_to_chain_runnable import run
from .part_2_how_to_stream_runnable import run
from .part_3_how_to_parallel_runnable import run


def lcel():
    loop.run_until_complete(run())