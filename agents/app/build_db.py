import os
import json
import uuid
import chromadb
from dotenv import load_dotenv
from zai import ZhipuAiClient


# 加载项目根目录下的 .env 文件
load_dotenv()
API_KEY = os.getenv("ZHIPUAI_API_KEY")

# 定义数据目录和向量数据库保存位置
DATA_DIR = "./data/Beijing Cultural Heritage"
DB_PATH = "./vector_db"

# 初始化智谱客户端
zhipu_client = ZhipuAiClient(api_key=API_KEY)

# 初始化 ChromaDB 客户端
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="museums_collection")


def get_zhipu_embedding(text):
    """调用智谱API获取文本的向量表示"""
    try:
        response = zhipu_client.embeddings.create(
            model="embedding-3",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"获取向量失败: {e}")
        return None


def process_and_store_data():
    """主逻辑：读取数据、清洗转换、向量化并入库"""
    links_file = os.path.join(DATA_DIR, "all_museum_links.json")

    if not os.path.exists(links_file):
        print(f"错误: 找不到总索引文件 {links_file}")
        return

    with open(links_file, 'r', encoding='utf-8') as f:
        museum_links = json.load(f)

    for item in museum_links:
        museum_name = item.get("name")
        if not museum_name:
            continue

        detail_file = os.path.join(DATA_DIR, f"{museum_name}.json")
        if not os.path.exists(detail_file):
            print(f"警告: 找不到 '{museum_name}' 的详情文件，已跳过。")
            continue

        with open(detail_file, 'r', encoding='utf-8') as f:
            museum_data = json.load(f)

        # 提取博物馆介绍（用于向量化）
        intro_text = museum_data.get("博物馆介绍", "")
        if not intro_text:
            print(f"警告: '{museum_name}' 缺少介绍字段，无法向量化，已跳过。")
            continue

        # 移除“所在地区”字段，保存其值用于后续填充
        region = museum_data.pop("所在地区", "未知")

        # 新增省级区划和市级区划
        museum_data["省级区划"] = "北京市"
        museum_data["市级区划"] = region

        # 生成该条数据的唯一ID
        museum_id = str(uuid.uuid4())

        print(f"正在处理并向量化: {museum_name} ...")
        embedding = get_zhipu_embedding(intro_text)

        if embedding is None:
            continue

        try:
            collection.add(
                ids=[museum_id],  # 唯一主键
                embeddings=[embedding],  # 智谱生成的向量
                documents=[intro_text],  # 原文本（RAG时直接召回此文本给大模型）
                metadatas=[museum_data]  # 其余所有字段作为元数据存入，方便后续结合条件过滤
            )
        except Exception as e:
            print(f"入库失败 '{museum_name}': {e}")

    print("🎉 所有数据清洗、向量化及入库操作已完成！")


if __name__ == "__main__":
    process_and_store_data()