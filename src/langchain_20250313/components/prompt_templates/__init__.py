from langchain_20250313.core import loop

from .part_1_how_to_use_few_shot_example import run
from .part_3_partially_prompt import run


def prompt():
    loop.run_until_complete(run())