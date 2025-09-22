# Interactive Debug Script Usage

## 🎮 BTC Price Prediction Game - Interactive Debugger

This script provides complete interactive debugging functionality, allowing you to manually control the game flow and observe all state changes in real-time.

## 🚀 Startup

1. **Start Server**:
   ```bash
   source venv/bin/activate
   python main.py
   ```

2. **Start Debug Script**:
   ```bash
   python interactive_debug.py
   ```

## ✨ Features

### 🔄 Auto Initialization
- Automatically reset all game data on startup
- Clear participant list and game state
- Verify server connection status

### 📝 Manual Participant Input
- Add participants one by one by entering UUIDs
- Display complete status JSON immediately after each input
- Real-time display of participant count (x/20)

### 📊 Complete Status Display
After each operation, the following will be displayed:
```json
{
  "status": 0,
  "realtime_price": 0.0,
  "final_price": 0.0,
  "balls": [...],
  "winner": ""
}
```

### 🔍 Auto Monitoring Mode
- Automatically start monitoring when 20 participants are reached
- Print complete status JSON every 2 seconds
- Real-time tracking of game progress and price changes

### 🏆 Auto Draw Detection
- Automatically detect game completion status
- Display winner information and final price
- Show detailed information of winning participants

## 📋 Available Commands

### Basic Operations
- **Enter UUID**: Directly enter UUID to add participants
- **quit**: Exit program
- **status <uuid>**: Manually query specific participant status

### Example Session
```
🎯 Enter UUID (participants: 0/20): player-001
✅ player-001 joined successfully! Assigned ball: B3
[Display complete JSON status]

🎯 Enter UUID (participants: 1/20): player-002
✅ player-002 joined successfully! Assigned ball: S7
[Display complete JSON status]

... (continue to 20 participants)

🎉 Game started with 20 participants!
🚀 Starting auto-monitoring mode...
[Auto display status every 2 seconds until draw]

🏆 LOTTERY DRAW COMPLETED!
🎊 Winner: B3
💰 Final Price: $100123.45
🎯 Winner Details:
   UUID: player-001
   Ball: B3
```

## 🎯 Game Flow Observation

### Preparation Phase (Status 0)
- Participants join one by one
- Ball numbers assigned but prices are 0
- Display number of assigned balls

### Game Phase (Status 1)  
- Automatically starts after 20th participant joins
- Calculate target prices for all balls based on initial BTC price
- Real-time price updates begin
- Auto monitoring mode starts

### Completion Phase (Status 2)
- Automatically detect draw completion
- Display winning ball and winner information
- Show final price

## 🛠️ Debug Features

### Error Handling
- Server connection check
- Duplicate UUID detection  
- Game full notification
- Network error recovery

### Real-time Feedback
- Immediate status feedback for each operation
- Detailed error messages
- Clear progress indicators

### Interrupt Handling
- Graceful exit with Ctrl+C
- Monitoring mode can be interrupted to return to manual mode
- Resource cleanup

## 💡 Usage Tips

1. **Step-by-step Observation**: Slowly add participants to observe ball assignment process
2. **Status Query**: Use `status <uuid>` to view specific participant status
3. **Monitoring Interrupt**: Press Ctrl+C during auto monitoring to return to manual mode
4. **Restart**: Restarting the script will automatically reset all data

## 🎪 Demo Scenarios

This script is particularly suitable for:
- Hackathon demo preparation
- API functionality verification
- Game flow testing
- Real-time status monitoring
- Draw logic verification

Perfect for showcasing the high-performance features of your async-hyperliquid library!
