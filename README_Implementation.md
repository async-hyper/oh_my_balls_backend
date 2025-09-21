# BTC Price Prediction Game - Implementation

## 项目概述

这是一个基于BTC价格预测的竞猜游戏，用于在hackathon的pitch环节展示我们的async-hyperliquid库的高性能特点。

## 项目结构

```
balls_game/
├── main.py                    # FastAPI应用入口
├── start_server.sh           # 服务器启动脚本
├── test_game.py              # API测试脚本
├── models/                   # 数据模型
│   ├── __init__.py
│   ├── ball.py              # 球分配模型
│   └── game.py              # 游戏状态模型
├── services/                 # 服务层
│   ├── __init__.py
│   ├── game_manager.py      # 游戏状态管理
│   ├── ball_calculator.py   # 球价格计算
│   ├── price_service.py     # 价格服务(待集成async-hyperliquid)
│   └── order_executor.py    # 订单执行(待集成async-hyperliquid)
├── websocket/               # WebSocket客户端
│   ├── __init__.py
│   └── hyperliquid_client.py # Hyperliquid WebSocket客户端
├── api/                     # API端点
│   ├── __init__.py
│   └── endpoints.py         # API端点实现
└── utils/                   # 工具函数
    ├── __init__.py
    └── helpers.py           # 辅助函数
```

## 快速开始

### 1. 激活虚拟环境
```bash
source venv/bin/activate
```

### 2. 启动服务器
```bash
./start_server.sh
```
或者直接运行：
```bash
python main.py
```

### 3. 测试API
```bash
python test_game.py
```

## API端点

### 1. 加入游戏
```http
POST /api/v1/join
Content-Type: application/json

{
  "uuid": "your-unique-id"
}
```

**响应:**
```json
{
  "ball": "B5"
}
```

### 2. 获取游戏状态
```http
GET /api/v1/status?uuid=your-unique-id
```

**响应:**
```json
{
  "status": 1,
  "realtime_price": 45000.50,
  "final_price": 0.0,
  "balls": [
    {
      "ball_name": "B0",
      "target_price": 45045.00
    }
  ],
  "winner": ""
}
```

### 3. 游戏信息
```http
GET /api/v1/game/info
```

## 游戏流程

1. **准备阶段 (status=0)**: 等待20个参与者加入
2. **游戏阶段 (status=1)**: 实时价格更新，30秒后执行订单
3. **完成阶段 (status=2)**: 显示获胜者和最终结果

## 集成点

### async-hyperliquid库集成
以下文件包含待集成的接口：

- `services/price_service.py`: BTC价格获取
- `services/order_executor.py`: 订单执行和取消
- `websocket/hyperliquid_client.py`: 订单状态监控

### 当前实现特点

- ✅ 完整的游戏状态管理
- ✅ 球分配和价格计算
- ✅ RESTful API接口
- ✅ 高频轮询支持
- ✅ 错误处理和状态验证
- 🔄 模拟价格数据 (待替换为真实数据)
- 🔄 模拟订单执行 (待替换为真实订单)
- 🔄 模拟WebSocket事件 (待替换为真实事件)

## 性能特点

- 支持20个参与者同时高频轮询 (100ms间隔)
- 异步处理，非阻塞I/O
- 内存存储，快速响应
- 实时价格更新和状态同步

## 开发说明

### 添加新的集成
1. 在相应的服务文件中实现真实的数据获取/订单执行逻辑
2. 替换模拟实现
3. 更新错误处理逻辑

### 测试
- 使用 `test_game.py` 进行API测试
- 支持单参与者和多参与者测试
- 包含完整游戏流程模拟

## 部署

这是一个一次性演示程序，设计为单服务器部署：
- 内存存储，无需数据库
- 支持20个并发用户
- 适合hackathon演示环境

## 下一步

1. 集成async-hyperliquid库进行真实价格获取
2. 集成async-hyperliquid库进行真实订单执行
3. 集成Hyperliquid WebSocket进行订单状态监控
4. 添加前端界面用于hackathon演示


