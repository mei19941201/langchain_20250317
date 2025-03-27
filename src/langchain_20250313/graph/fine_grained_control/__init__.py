from langchain_20250313.core import loop

from .part_1_map_reduce import run
from .part_2_update_and_goto import run, run2
from .part_3_how_to_add_runnable_config_to_graph import run

def fine_grianed_control():
    loop.run_until_complete(run())