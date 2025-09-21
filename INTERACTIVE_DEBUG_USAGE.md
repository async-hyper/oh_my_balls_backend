# Interactive Debug Script Usage

## 🎮 BTC Price Prediction Game - Interactive Debugger

这个脚本提供了完整的交互式调试功能，让您可以手动控制游戏流程并实时观察所有状态变化。

## 🚀 启动方式

1. **启动服务器**：
   ```bash
   source venv/bin/activate
   python main.py
   ```

2. **启动调试脚本**：
   ```bash
   python interactive_debug.py
   ```

## ✨ 功能特点

### 🔄 自动初始化
- 每次启动时自动重置所有游戏数据
- 清空参与者列表和游戏状态
- 验证服务器连接状态

### 📝 手动参与者输入
- 逐个输入UUID添加参与者
- 每次输入后立即显示完整的status JSON
- 实时显示参与者数量 (x/20)

### 📊 完整状态显示
每次操作后都会显示：
```json
{
  "status": 0,
  "realtime_price": 0.0,
  "final_price": 0.0,
  "balls": [...],
  "winner": ""
}
```

### 🔍 自动监控模式
- 达到20个参与者时自动启动监控
- 每2秒打印一次完整的status JSON
- 实时跟踪游戏进度和价格变化

### 🏆 自动开奖检测
- 自动检测游戏完成状态
- 显示获胜者信息和最终价格
- 展示获胜参与者的详细信息

## 📋 可用命令

### 基本操作
- **输入UUID**: 直接输入UUID来添加参与者
- **quit**: 退出程序
- **status <uuid>**: 手动查询特定参与者的状态

### 示例会话
```
🎯 Enter UUID (participants: 0/20): player-001
✅ player-001 joined successfully! Assigned ball: B3
[显示完整JSON状态]

🎯 Enter UUID (participants: 1/20): player-002
✅ player-002 joined successfully! Assigned ball: S7
[显示完整JSON状态]

... (继续到20个参与者)

🎉 Game started with 20 participants!
🚀 Starting auto-monitoring mode...
[每2秒自动显示状态直到开奖]

🏆 LOTTERY DRAW COMPLETED!
🎊 Winner: B3
💰 Final Price: $100123.45
🎯 Winner Details:
   UUID: player-001
   Ball: B3
```

## 🎯 游戏流程观察

### 准备阶段 (Status 0)
- 参与者逐个加入
- 球号码分配但价格为0
- 显示已分配的球数量

### 游戏阶段 (Status 1)  
- 第20个参与者加入后自动开始
- 根据初始BTC价格计算所有球的目标价格
- 实时价格开始更新
- 自动监控模式启动

### 完成阶段 (Status 2)
- 自动检测开奖完成
- 显示获胜球和获胜者信息
- 展示最终价格

## 🛠️ 调试特性

### 错误处理
- 服务器连接检查
- 重复UUID检测  
- 游戏满员提示
- 网络错误恢复

### 实时反馈
- 每个操作的即时状态反馈
- 详细的错误信息
- 清晰的进度指示器

### 中断处理
- Ctrl+C 优雅退出
- 监控模式可中断返回手动模式
- 资源清理

## 💡 使用技巧

1. **逐步观察**: 慢慢添加参与者，观察球分配过程
2. **状态查询**: 使用 `status <uuid>` 查看特定参与者状态
3. **监控中断**: 在自动监控时按Ctrl+C返回手动模式
4. **重新开始**: 重启脚本会自动重置所有数据

## 🎪 演示场景

这个脚本特别适合：
- Hackathon演示准备
- API功能验证
- 游戏流程测试
- 实时状态监控
- 开奖逻辑验证

完美展示您的async-hyperliquid库的高性能特点！
