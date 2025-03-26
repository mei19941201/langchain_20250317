from langchain_20250313.core import loop

from .part_1_how_to_update_state_from_node import run
from .part_2_how_to_create_sequence_step_graph import run
from .part_3_how_to_create_branch import run, run2
from .part_4_how_to_create_and_control_loop import run, run2


def graph_guide():
    loop.run_until_complete(run2())