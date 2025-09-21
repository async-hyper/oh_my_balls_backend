from pydantic import BaseModel
from typing import Literal
from enum import Enum

class BallType(str, Enum):
    LONG = "long"
    SHORT = "short"

class BallAssignment(BaseModel):
    ball_name: str  # "B0"-"B9" or "S0"-"S9"
    target_price: float  # Calculated target price for this ball
    uuid: str  # Owner's UUID
    position: BallType  # "long" or "short"
    order_id: str = None  # Order ID when placed via async-hyperliquid

    class Config:
        use_enum_values = True

