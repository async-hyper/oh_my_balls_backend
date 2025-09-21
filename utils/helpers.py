import uuid
import re
from typing import Optional

def generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid.uuid4())

def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format"""
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(uuid_string))

def format_price(price: float) -> float:
    """Format price to 2 decimal places"""
    return round(price, 2)

def calculate_price_difference(current_price: float, target_price: float) -> float:
    """Calculate percentage difference between current and target price"""
    if target_price == 0:
        return 0
    return ((current_price - target_price) / target_price) * 100


