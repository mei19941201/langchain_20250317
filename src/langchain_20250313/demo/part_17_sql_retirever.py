from langchain_20250313.core import llm, embedding, logger, db

from langchain.chains import create_sql_query_chain



def part17():
    chain = create_sql_query_chain(llm, db)
    res = chain.invoke({"question": "查询agent_tool表中的全部数据。"})
    logger.info(res)