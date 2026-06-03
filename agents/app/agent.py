import os
import json
from typing import Annotated, Literal
from typing_extensions import TypedDict

# 导入 LangGraph 相关组件
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from duckduckgo_search import DDGS

import chromadb
from dotenv import load_dotenv

from zai import ZhipuAiClient


load_dotenv()
API_KEY = os.getenv("ZHIPUAI_API_KEY")

zhipu_client = ZhipuAiClient(api_key=API_KEY)
chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection(name="museums_collection")


# 定义具体工具函数 (Tools)
def web_search(query: str) -> str:
    """调用原生的 DuckDuckGo 搜索引擎获取实时信息"""
    print(f"🛠️ [Tool执行] 正在联网搜索实时信息: {query}")
    try:
        # 使用 DDGS 原生客户端
        with DDGS() as ddgs:
            # max_results 可以限制返回结果的数量，避免大模型 Token 超出限制
            results = ddgs.text(query, max_results=3)

            if not results:
                return "未搜索到相关实时信息。"

            # 手动提取并格式化要给大模型看的信息
            formatted_results = []
            for r in results:
                title = r.get('title', '无标题')
                body = r.get('body', '无内容摘要')
                href = r.get('href', '无链接')
                formatted_results.append(f"【{title}】\n摘要: {body}\n来源链接: {href}\n")

            return "\n".join(formatted_results)

    except Exception as e:
        return f"联网搜索失败: {str(e)}"


def rag_search(query: str) -> str:
    """从 ChromaDB 向量数据库中检索北京博物馆信息"""
    print(f"🛠️ [Tool执行] 正在向量数据库中检索: {query}")
    try:
        # 向量化查询语句
        response = zhipu_client.embeddings.create(
            model="embedding-3",
            input=query
        )
        query_embedding = response.data[0].embedding

        # 检索 ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3  # 召回前3条最相关数据
        )

        # 格式化组装召回的上下文
        if not results['documents'][0]:
            return "本地数据库中未找到相关的博物馆信息。"

        context_parts = []
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]

            # 提取元数据中的信息
            prov = meta.get("省级区划", "未知")
            city = meta.get("市级区划", "未知")
            name = meta.get("name", "未知博物馆")

            context_parts.append(
                f"【{name}】(位置: {prov}{city})\n介绍: {doc}\n"
            )

        return "\n".join(context_parts)
    except Exception as e:
        return f"检索本地数据库时出错: {str(e)}"


tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": "当用户询问北京当地文化遗产、博物馆的历史背景、馆藏介绍、基本概况时，调用此工具从本地数据库检索。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用于在向量数据库中检索的查询语句"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "当用户询问实时的展览信息、门票价格、近期新闻、天气情况等动态内容时，调用此工具进行全网搜索。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用于在搜索引擎中查询的关键词"}
                },
                "required": ["query"]
            }
        }
    }
]

# 定义状态存储：记录所有的对话消息
class State(TypedDict):
    messages: Annotated[list, add_messages]


def call_zhipu_agent(state: State):
    """Agent节点：负责思考、回答，以及决定是否调用工具"""
    messages = state["messages"]

    zhipu_msgs = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            zhipu_msgs.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            m = {"role": "assistant", "content": msg.content or ""}
            # 如果之前有工具调用，需要带上 tool_calls
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                m["tool_calls"] = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {"name": tc["name"], "arguments": json.dumps(tc["args"])}
                    } for tc in msg.tool_calls
                ]
            zhipu_msgs.append(m)
        elif isinstance(msg, ToolMessage):
            zhipu_msgs.append({
                "role": "tool",
                "tool_call_id": msg.tool_call_id,
                "content": msg.content
            })

    # 调用原生智谱 API
    response = zhipu_client.chat.completions.create(
        model="glm-4.5-air",
        messages=zhipu_msgs,
        tools=tools_schema
    )

    response_msg = response.choices[0].message

    # 消息转换：将智谱 API 返回的结果转回 LangChain 的 AIMessage
    if response_msg.tool_calls:
        # 解析工具调用信息
        lc_tool_calls = [
            {
                "name": tc.function.name,
                "args": json.loads(tc.function.arguments),
                "id": tc.id
            } for tc in response_msg.tool_calls
        ]
        return {"messages": [AIMessage(content=response_msg.content or "", tool_calls=lc_tool_calls)]}
    else:
        return {"messages": [AIMessage(content=response_msg.content)]}


def execute_tools(state: State):
    """Tool节点：负责具体执行 Agent 决定的工具函数"""
    last_message = state["messages"][-1]
    results = []

    # 遍历执行所有需要调用的工具
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        if tool_name == "rag_search":
            result_str = rag_search(tool_args["query"])
        elif tool_name == "web_search":
            result_str = web_search(tool_args["query"])
        else:
            result_str = f"未知的工具: {tool_name}"

        # 将结果封装为 ToolMessage 返回给状态机
        results.append(ToolMessage(content=result_str, tool_call_id=tool_id))

    return {"messages": results}


def route_decision(state: State) -> Literal["tools", END]:
    """条件路由：判断模型是否请求了工具调用"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# 编译与运行 Graph、
# noinspection PyTypeChecker
workflow = StateGraph(State)

# 添加节点
# noinspection PyTypeChecker
workflow.add_node("agent", call_zhipu_agent)
# noinspection PyTypeChecker
workflow.add_node("tools", execute_tools)

# 设置边与路由
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    route_decision,
    {"tools": "tools", END: END}
)
workflow.add_edge("tools", "agent")

app = workflow.compile()


if __name__ == "__main__":
    print("🤖 博物馆智能体已启动！输入 'quit' 退出。")
    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ['quit', 'exit']:
            break

        # 调用流式处理，便于观察调用轨迹
        for event in app.stream({"messages": [HumanMessage(content=user_input)]}):
            for node_name, node_state in event.items():
                if node_name == "agent":
                    msg = node_state["messages"][-1]
                    if not msg.tool_calls:
                        print(f"\n💡 智能体: {msg.content}")