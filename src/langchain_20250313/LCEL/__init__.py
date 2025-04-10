from langchain_20250313.core import loop

from .part_1_how_to_chain_runnable import run
from .part_2_how_to_stream_runnable import run
from .part_3_how_to_parallel_runnable import run
from .part_4_how_to_add_default_args_to_runnable import run
from .part_5_how_to_turn_func_to_runnable import run
from .part_7_how_to_configure_runnable import run
from .part_9_how_to_route_chain import run


def lcel():
    loop.run_until_complete(run())