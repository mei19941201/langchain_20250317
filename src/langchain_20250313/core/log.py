import logging
from loguru import logger


logger.remove(0)
logger.add("./log/langchain.log", mode="w")