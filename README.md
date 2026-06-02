# 博物馆推荐系统 — 前后端架构

基于大语言模型的博物馆推荐与旅行规划系统。本仓库实现**前后端分离架构**：前端中国行政区划地图 + 省级对话页，Spring Boot 后端网关，调用 Python 实现的省级智能体服务。

## 架构概览

```
┌─────────────┐     HTTP      ┌──────────────────┐     HTTP      ┌─────────────────┐
│  React 前端  │ ────────────► │ Spring Boot 后端  │ ────────────► │ Python 智能体    │
│  中国地图    │   /api/chat   │  省份路由 / CORS  │  /api/v1/chat │  FastAPI (可接LLM)│
│  省级对话    │               │                  │               │                  │
└─────────────┘               └──────────────────┘               └─────────────────┘
```

## 目录结构

| 目录 | 说明 |
|------|------|
| `frontend/` | React + Vite + ECharts 中国地图与聊天界面 |
| `backend/` | Spring Boot 3 REST API，转发请求至 Python 智能体 |
| `agents/` | FastAPI 省级智能体（当前为桩实现，可接入 LLM/RAG） |

## 本地运行

### 1. Python 智能体（端口 8000）

```bash
cd agents
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

验证：访问 http://localhost:8000/health

### 2. Spring Boot 后端（端口 8080）

需要 JDK 17+ 与 Maven。

```bash
cd backend
mvn spring-boot:run
```

环境变量（可选）：

- `AGENT_BASE_URL`：智能体地址，默认 `http://localhost:8000`

### 3. React 前端（端口 5173）

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173 ，点击地图省份进入对话页。

开发模式下 Vite 已将 `/api` 代理到 `http://localhost:8080`。

## API 说明

### 省份列表

`GET /api/provinces`

### 省级对话

`POST /api/chat/{provinceCode}`

请求体：

```json
{ "message": "周末两天想参观历史类博物馆" }
```

请求头（可选）：`X-Session-Id` — 会话标识，用于后续多轮对话扩展。

响应：

```json
{
  "reply": "...",
  "provinceCode": "beijing",
  "provinceName": "北京市",
  "suggestions": ["...", "..."]
}
```

### 智能体内部接口（Spring Boot 调用）

`POST /api/v1/chat`（Python 服务）

```json
{
  "province_code": "beijing",
  "province_name": "北京市",
  "message": "用户问题",
  "session_id": "uuid"
}
```

## Docker 一键启动

```bash
docker compose up --build
```

- 前端：http://localhost:5173  
- 后端：http://localhost:8080  
- 智能体：http://localhost:8000  

## 与知识库 / LLM 的对接

在 `agents/app/province_agent.py` 中替换 `generate_reply` 实现：

1. 根据 `province_code` 加载省级知识库索引  
2. 对用户 `message` 做 RAG 检索  
3. 调用大语言模型生成推荐与行程规划  
4. 保持 `ChatResponse` 的 `reply` 与 `suggestions` 字段不变，无需修改 Spring Boot 与前端  

## 技术栈

- **前端**：React 18、TypeScript、Vite、ECharts 5、React Router  
- **后端**：Spring Boot 3.3、Java 17、RestTemplate  
- **智能体**：FastAPI、Uvicorn、Pydantic  
