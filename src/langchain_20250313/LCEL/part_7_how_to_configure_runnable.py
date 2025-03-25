from langchain_20250313.core import llm, logger

from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser


configurable_llm = llm.configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="temperature",
        description="temperature of model sample"
    ),
    top_p=ConfigurableField(
        id="top_p",
        name="top_p",
        description="top_p of model sample"
    )
)


async def run():

    chain = configurable_llm | StrOutputParser() | (lambda x: logger.info(x))

    for i in [0, 10]:
        chain.with_config({"configurable": {"temperature": i}}).invoke("下一首关于秋天的四言绝句。")
