from langchain_20250313.core import llm, logger


async def run():
    res = await llm.ainvoke("海内存知己下一句")
    logger.info(res.usage_metadata)