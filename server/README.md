
## QuickNote Server


### 项目描述

微软曾经推出一个Recall，但是因为隐私和高资源消耗而没有收到用户的喜欢。我想开发一个类似的功能的项目，项目架构采用 server-client 模式，用户可以在不同的client（ios, android, pc）触发截图，并且将截图+要提取的内容的prompt一起传给server，server使用fastapi技术开发，并且可以调用 LLM 进行解析和内容提取，然后将提取后的内容我会通过 API 调用存到我自己部署的 memos 项目中。

### 项目技术栈
服务器开发采用 fastapi, 然后python库管理采用 uv 。

# 服务器开发说明
1. 提供最基本的接口用于接受 client 发起的请求，接受图片+prompt
2. 通过 .env 配置调用 ollama / openai / gemini / claude 相关 vision-language 模型进行解析。
3. 将解析结果调用 memos 相关的 API 进行存储和展示。

### 环境变量

`.env` 示例（已提供 `.env`，直接修改即可）：
```
PROVIDER=ollama
SYSTEM_PROMPT=Return Markdown using lines that start with URL:, Title:, and Desc: (Desc can span multiple lines). Do not return JSON.
MEMOS_BASE_URL=https://note.zimu.info
MEMOS_TOKEN=your_token_here

OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com
OPENAI_MODEL=gpt-4o-mini

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3-vl
```

### 接口说明

- `POST /v1/image/data`：`multipart/form-data`，字段 `image`、`prompt`、`upload_to_memos`（bool）、`provider`（可选）
- `POST /v1/image/json`：JSON body，字段 `image_base64`、`prompt`、`upload_to_memos`、`provider`（可选）、`filename`、`content_type`
- 当 `upload_to_memos=true` 时：先上传附件，再创建 memo，最后调用 Set Memo Attachments 绑定二者。
- `provider` 支持 `openai` / `ollama`，不传则使用 `.env` 中的 `PROVIDER`。
- memo 模版固定为 `URL` / `Title` / `Desc` 三部分，系统提示词需按该格式返回 Markdown。

### 本地开发

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```bash
pytest
```

### memeos 相关

1. memeos 被部署在 https://note.zimu.info/

2. 相关的 API 调用接口示例

- 创建memo
```bash
curl --location --request POST 'https://note.zimu.info/api/v1/memos' \
--header 'Content-Type: application/json' \
--header 'Authorization: <MEMOS_ACCESS_TOKEN>' \
--data-raw '{
    "state": "STATE_UNSPECIFIED",
    "content": "test content --- \n hello ** world **",
    "visibility": "VISIBILITY_UNSPECIFIED"
}'
```

- 上传附件

```
curl https://note.zimu.info/api/v1/attachments \
  -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "test_mem.png",
    "type": "image/png",
    "content": "'"$(cat test_mem.png.b64)"'"
  }'
  ```
