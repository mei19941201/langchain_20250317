from .server import server
from .demo.part_2_message import part2
from .demo.part_4_tools import part4
from .demo.part_6_structure_output import part6
from .demo.part_9_runnable import part9
# from .demo.part_13_retrieval import part13
# from .demo.part_13_retrieval2 import part13_2
# from .demo.part_17_sql_retirever import part17

from .components.chat_model import chat_model



import torch


def cuda():
    r = torch.cuda.is_available()
    print(r)