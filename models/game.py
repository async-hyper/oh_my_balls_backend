from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .ball import BallAssignment

class GameStatus(int):
    PREPARING = 0
    DRAWING = 1
    DONE = 2

class GameState(BaseModel):
    game_id: str
    status: int  # 0: preparing, 1: drawing, 2: done
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    initial_price: Optional[float] = None
    final_price: Optional[float] = None
    current_price: Optional[float] = None
    balls: List[BallAssignment] = []
    participants: Dict[str, str] = {}  # uuid -> ball_name
    winner: Optional[str] = None  # Winning ball name
    placed_orders: List[str] = []  # List of order IDs placed via async-hyperliquid
    filled_order: Optional[str] = None  # Order ID of the first filled order
    hyperliquid_ws_connected: bool = False
    price_history: List[Dict[str, float]] = []  # List of {timestamp: timestamp, price: price} objects
    price_counter: int = 0  # Sequential counter for unique timestamps

    class Config:
        use_enum_values = True
