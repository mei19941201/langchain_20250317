from langchain_20250313.core import loop

from .part_1_how_to_use_tool import run
from .part_2_how_to_return_structured_data_from_llm import run
from .part_3_hot_to_cache_model_response import run
from .part_4_hot_to_get_log_prob import run
from .part_6_how_to_stream_model_response import run
from .part_7_how_to_trace_token_usage import run
from .part_11_how_to_handle_rate_limit import run
from .part_12_how_to_few_shot_prompt_tool_behavior import run
from .part_13_how_to_bind_model_specific_formatted_tools import run
from .part_14_how_to_force_a_tool_call import run
from .part_16_how_to_init_any_model_in_one_line import run


def chat_model():
    loop.run_until_complete(run())