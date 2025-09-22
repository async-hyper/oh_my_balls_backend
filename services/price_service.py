from async_hyper import AsyncHyper


class PriceService:
    """Service for fetching BTC price data"""

    def __init__(self, async_hyper: AsyncHyper):
        self.async_hyper = async_hyper

    async def get_current_price(self) -> float:
        """
        Get current BTC perp market price
        """
        price = await self.async_hyper.get_market_price("BTC")
        return price

    async def get_initial_price(self) -> float:
        """Get initial price for game start"""
        return await self.get_current_price()
