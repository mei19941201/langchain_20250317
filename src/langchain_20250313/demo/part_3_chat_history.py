from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)


s1 = [
    SystemMessage(""),
    HumanMessage(""),
    AIMessage(""),
]


s2 = [
    SystemMessage(""),
    HumanMessage(""),
    AIMessage(""),
    ToolMessage(""),
    AIMessage(""),
]


good_structure = [
    # 必须系统或用户信息开头，用户信息结尾。

    # 第一种
    SystemMessage(""),
    HumanMessage(""),
    AIMessage(""),
    HumanMessage(""),

    # 第二种
    HumanMessage(""),
    AIMessage(""),
    HumanMessage(""),

    # 第三种，ai消息后紧跟tool消息
    HumanMessage(""),
    AIMessage(""),
    ToolMessage(""),
    AIMessage(""),
    HumanMessage(""),

]