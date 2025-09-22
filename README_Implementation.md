# BTC Price Prediction Game - Implementation

## Project Overview

This is a BTC price prediction guessing game designed to showcase the high-performance features of our async-hyperliquid library during hackathon pitch sessions.

## Project Structure

```
balls_game/
├── main.py                    # FastAPI application entry point
├── start_server.sh           # Server startup script
├── test_game.py              # API test script
├── models/                   # Data models
│   ├── __init__.py
│   ├── ball.py              # Ball assignment model
│   └── game.py              # Game state model
├── services/                 # Service layer
│   ├── __init__.py
│   ├── game_manager.py      # Game state management
│   ├── ball_calculator.py   # Ball price calculation
│   ├── price_service.py     # Price service (to integrate async-hyperliquid)
│   └── order_executor.py    # Order execution (to integrate async-hyperliquid)
├── websocket/               # WebSocket client
│   ├── __init__.py
│   └── hyperliquid_client.py # Hyperliquid WebSocket client
├── api/                     # API endpoints
│   ├── __init__.py
│   └── endpoints.py         # API endpoint implementation
└── utils/                   # Utility functions
    ├── __init__.py
    └── helpers.py           # Helper functions
```

## Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Start Server
```bash
./start_server.sh
```
Or run directly:
```bash
python main.py
```

### 3. Test API
```bash
python test_game.py
```

## API Endpoints

### 1. Join Game
```http
POST /api/v1/join
Content-Type: application/json

{
  "uuid": "your-unique-id"
}
```

**Response:**
```json
{
  "ball": "B5"
}
```

### 2. Get Game Status
```http
GET /api/v1/status?uuid=your-unique-id
```

**Response:**
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

### 3. Game Information
```http
GET /api/v1/game/info
```

## Game Flow

1. **Preparation Phase (status=0)**: Wait for 20 participants to join
2. **Game Phase (status=1)**: Real-time price updates, execute orders after 30 seconds
3. **Completion Phase (status=2)**: Display winner and final results

## Integration Points

### async-hyperliquid Library Integration
The following files contain interfaces to be integrated:

- `services/price_service.py`: BTC price fetching
- `services/order_executor.py`: Order execution and cancellation
- `websocket/hyperliquid_client.py`: Order status monitoring

### Current Implementation Features

- ✅ Complete game state management
- ✅ Ball assignment and price calculation
- ✅ RESTful API interface
- ✅ High-frequency polling support
- ✅ Error handling and state validation
- 🔄 Simulated price data (to be replaced with real data)
- 🔄 Simulated order execution (to be replaced with real orders)
- 🔄 Simulated WebSocket events (to be replaced with real events)

## Performance Features

- Supports 20 participants with high-frequency polling (100ms intervals)
- Asynchronous processing, non-blocking I/O
- In-memory storage, fast response
- Real-time price updates and state synchronization

## Development Notes

### Adding New Integrations
1. Implement real data fetching/order execution logic in corresponding service files
2. Replace simulated implementations
3. Update error handling logic

### Testing
- Use `test_game.py` for API testing
- Supports single and multiple participant testing
- Includes complete game flow simulation

## Deployment

This is a one-time demo program designed for single-server deployment:
- In-memory storage, no database required
- Supports 20 concurrent users
- Suitable for hackathon demo environments

## Next Steps

1. Integrate async-hyperliquid library for real price fetching
2. Integrate async-hyperliquid library for real order execution
3. Integrate Hyperliquid WebSocket for order status monitoring
4. Add frontend interface for hackathon demo


