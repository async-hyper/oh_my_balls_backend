# Balls Game API

一个使用 FastAPI 构建的简单后端 API 项目。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
# 方法1: 使用 uvicorn 命令
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方法2: 直接运行 main.py
python main.py
```

## API 端点

- `GET /` - Hello World 端点
- `GET /health` - 健康检查端点
- `GET /docs` - Swagger UI 文档 (自动生成)

## 访问 API

启动后，你可以通过以下地址访问：

- API 基础地址: http://localhost:8000
- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

## 测试 API

```bash
# 测试 Hello World 端点
curl http://localhost:8000/

# 测试健康检查端点
curl http://localhost:8000/health
```



