import asyncio
import random
from typing import Optional

class PriceService:
    """Service for fetching BTC price data"""
    
    def __init__(self):
        self.base_price = 100000.0  # Simulated base price for testing
        self.price_variance = 0.02  # 2% variance
    
    async def get_current_price(self) -> float:
        """
        Get current BTC price
        TODO: Integrate with async-hyperliquid library
        """
        # Simulate price movement around base price
        variance = random.uniform(-self.price_variance, self.price_variance)
        current_price = self.base_price * (1 + variance)
        
        # Simulate some price trending
        self.base_price += random.uniform(-100, 100)
        
        return round(current_price, 2)
    
    async def get_initial_price(self) -> float:
        """Get initial price for game start"""
        return await self.get_current_price()
