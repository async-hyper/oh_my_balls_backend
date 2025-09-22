# BTC Price Prediction Game API Design

## Overview

This document outlines the API design for a BTC price prediction game designed to showcase the performance characteristics of our HyperEVM SDK wrapper library. The game demonstrates async execution, request batching, and smart contract integration for a hackathon pitch presentation.

## Game Flow

1. **Setup Phase**: QR code displayed to audience for game participation
2. **Registration Phase**: First 20 participants receive random ball assignments
   - B0-B9: Green balls for "long" positions (10 balls)
   - S0-S9: Red balls for "short" positions (10 balls)
3. **Game Phase**: 
   - Price fixed at t0 with p0 BTC-USD price
   - Balls positioned on grid, price level highlighted every 100ms
   - Current winning ball highlighted in real-time
4. **Execution Phase**: After 30 seconds
   - 20 orders placed asynchronously using async-hyperliquid library
   - Hyperliquid WebSocket monitors order execution status
   - First order to fill triggers cancellation of remaining 19 orders
   - Winner determined by the ball corresponding to the filled order's price
5. **Conclusion**: Winner announced, ball owner receives reward

## API Endpoints

### 1. Join Game

**Endpoint**: `/join`  
**Method**: `POST`  
**Description**: Register a participant and receive a ball assignment

#### Request Body
```json
{
  "uuid": "string"
}
```

#### Response
```json
{
  "ball": "string"  // Ball name format: "B0", "B1", ..., "B9" or "S0", "S1", ..., "S9"
}
```

#### Business Logic
- Accepts first 20 unique UUIDs
- Randomly assigns balls (10 long "B" balls, 10 short "S" balls)
- Returns 409 Conflict if game is full
- Returns 400 Bad Request for invalid UUID format

---

### 2. Game Status

**Endpoint**: `/status`  
**Method**: `GET`  
**Description**: Get current game status and real-time information

#### Request Parameters
None - This endpoint is publicly accessible

#### Response
```json
{
  "status": 0,                    // 0: preparing, 1: drawing, 2: done
  "realtime_price": 0.0,          // Current BTC-USD price
  "final_price": 0.0,             // Final price at game end (0.0 if not finished)
  "balls": [                      // Array of ball assignments and their target prices
    {
      "ball_name": "B0",
      "target_price": 45000.50
    },
    {
      "ball_name": "S1", 
      "target_price": 44950.25
    }
    // ... up to 20 balls
  ],
  "winner": "string"              // Winning ball name (empty if game not finished)
}
```

#### Business Logic
- Status 0: Game preparation, waiting for 20 participants
- Status 1: Active game, showing real-time price updates every 100ms
- Status 2: Game completed, showing final results
- Returns 404 Not Found if no active game exists
- Publicly accessible - no authentication required

## Data Models

### Ball Assignment
```json
{
  "ball_name": "string",    // "B0"-"B9" or "S0"-"S9"
  "target_price": "float",  // Calculated target price for this ball
  "uuid": "string"          // Owner's UUID
}
```

### Game State
```json
{
  "game_id": "string",           // Unique game identifier
  "status": "integer",           // 0, 1, or 2
  "start_time": "datetime",      // Game start timestamp
  "end_time": "datetime",        // Game end timestamp (null if ongoing)
  "initial_price": "float",      // BTC price at game start
  "final_price": "float",        // BTC price at game end
  "balls": "array",              // Array of BallAssignment objects
  "winner": "string"            // Winning ball name
}
```

## Implementation Architecture

### Core Components

1. **Game Manager**: Handles game state, ball assignments, and status transitions
2. **Price Service**: [TO BE INTEGRATED] - Will use async-hyperliquid library for BTC price data
3. **Ball Calculator**: Determines target prices for each ball based on initial price
4. **Order Executor**: [TO BE INTEGRATED] - Will use async-hyperliquid library for place/cancel orders
5. **Hyperliquid WebSocket Client**: Subscribes to order execution events to determine winner
6. **Status Handler**: Provides real-time game status via repeated API calls

### Technology Stack

- **Framework**: FastAPI (Python)
- **Async Runtime**: asyncio
- **WebSocket**: Hyperliquid WebSocket (for order tracking only)
- **Price Data**: [TO BE INTEGRATED] - async-hyperliquid library
- **Order Execution**: [TO BE INTEGRATED] - async-hyperliquid library
- **Order Tracking**: [TO BE INTEGRATED] Hyperliquid WebSocket for real-time order status

### Database Schema (In-Memory)

```python
# Game state stored in memory for simplicity
games = {
    "game_id": {
        "status": 0,
        "participants": {},  # uuid -> ball_name
        "balls": [],         # BallAssignment objects
        "start_time": None,
        "initial_price": None,
        "current_price": None,
        "winner": None,
        "placed_orders": [],  # List of order IDs placed via async-hyperliquid
        "filled_order": None, # Order ID of the first filled order
        "hyperliquid_ws_connected": False
    }
}
```

## Error Handling

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request format or parameters
- `404 Not Found`: UUID not found or game doesn't exist
- `409 Conflict`: Game is full or already started
- `500 Internal Server Error`: Server-side error

### Error Response Format

```json
{
  "error": "string",        // Error message
  "code": "string",         // Error code
  "details": "object"       // Additional error details
}
```

## Hyperliquid Integration

### Order Execution Flow

1. **Order Placement**: After 30 seconds, place 20 orders asynchronously using async-hyperliquid library
2. **WebSocket Subscription**: Subscribe to Hyperliquid WebSocket for order execution events
3. **Order Monitoring**: Monitor all 20 placed orders for fill status
4. **Winner Detection**: When first order fills:
   - Identify the ball corresponding to the filled order's price
   - Cancel remaining 19 orders immediately by async-hyperliquid library [TO-BE-INTEGRATION]
   - Announce winner based on filled order price
5. **Price Matching**: Match filled order price to closest ball target price

### Hyperliquid WebSocket Events

- `order_fill`: Real-time notification when any order gets filled
- `order_cancel`: Confirmation when orders are successfully cancelled
- `order_reject`: Notification if any order gets rejected


## Real-Time Updates

### Client Update Strategy

Clients will poll the `/status` endpoint repeatedly to get real-time updates:

- **Polling Frequency**: Every 100ms during active game (status = 1)
- **Polling Frequency**: Every 1 second during preparation phase (status = 0)
- **Polling Frequency**: Every 5 seconds after game completion (status = 2)

### Status API Response Updates

The `/status` endpoint will return updated information including:

- `realtime_price`: Current BTC price (updated every 100ms during game)
- `status`: Game phase indicator (0: preparing, 1: drawing, 2: done)
- `balls`: Array with current winning ball highlighted
- `winner`: Set when game completes with filled order details


## Security Considerations

Do not concern about any security issues because this is an one-time program.

## Performance Requirements

- **Concurrent Users**: Support up to 20 simultaneous participants
- **Price Updates**: 100ms intervals during active game (via async-hyperliquid)
- **Order Placement**: All 20 orders placed within 1 second (via async-hyperliquid)
- **Order Tracking**: Real-time order status updates via Hyperliquid WebSocket
- **Order Cancellation**: Remaining 19 orders cancelled within 500ms after first fill (via async-hyperliquid)

## Testing Strategy

### Unit Tests
- Ball assignment logic
- Price calculation algorithms
- Status transition validation
- Error handling scenarios
- Order tracking logic
- Winner determination based on filled order price


## Deployment Considerations

- **Environment**: Single server deployment for hackathon demo
- **Monitoring**: Basic logging for game events and errors
- **Scaling**: Not required for demo purposes
- **Persistence**: In-memory storage sufficient for demo

---

*This API design prioritizes simplicity and demonstration value for the hackathon pitch while maintaining the exact field specifications as requested.*
