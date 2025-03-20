from langchain_20250313.core import loop

from .part_1_how_to_trim_message import run, run1
from .part_2_how_to_filter_message import run
from .part_3_how_to_merge_message import run


def messages():
    loop.run_until_complete(run())