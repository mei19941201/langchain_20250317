from langchain_20250313.core import llm, logger

import os
from langchain.chat_models import init_chat_model

async def run():
    
    # 重要的是configurable_fields，这个参事可以在运行时动态的传入参数，更改模型参数。
    llm = init_chat_model(
        model=os.environ["CHAT_MODEL"],
        model_provider="openai",
        api_key=os.environ["CHAT_API_KEY"],
        base_url=os.environ["CHAT_BASE_URL"],
        temperature=1,
        configurable_fields=[
            "temperature"
        ]
    )

    res = await llm.ainvoke("你好啊", config={"configurable": {"temperature": 4}})
    logger.info(res)

    res = await llm.ainvoke("你好啊", config={"configurable": {"temperature": 0}})
    logger.info(res)