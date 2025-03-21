from langchain_20250313.core import loop

from .part_1_parse_text_from_message import run
from .part_2_parse_structured_format import run


def parser():
    loop.run_until_complete(run())