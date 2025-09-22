import asyncio
import json
from typing import List, Optional

import websockets
from async_hyper import AsyncHyper

from models.ball import BallAssignment, BallType


def parse_order_info(resp: dict) -> str:
    return resp["response"]["data"]["statuses"][0]["resting"]


class OrderExecutor:
    """Service for executing orders via async-hyperliquid library"""

    def __init__(self, async_hyper: AsyncHyper):
        self.order_counter = 0
        self.async_hyper = async_hyper
        self.coin = "BTC"

    async def place_orders(self, balls: List[BallAssignment]) -> List[str]:
        """
        Place all 20 orders asynchronously
        """
        order_ids = []

        mark_px = await self.async_hyper.get_market_price(self.coin)

        tasks = []
        for ball in balls:
            ball_name = ball.ball_name
            ball.position = (
                BallType.LONG if ball_name.startswith("B") else BallType.SHORT
            )

            offset = int(ball_name[-1:]) + 1
            if ball.position == BallType.LONG:
                ball.target_price = mark_px - offset
            else:
                ball.target_price = mark_px + offset

            task = asyncio.create_task(self._place_single_order(ball))
            tasks.append(task)

        # Wait for all orders to be placed
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, str):
                order_ids.append(result)
            else:
                print(f"Order placement failed: {result}")

        return order_ids

    async def _place_single_order(self, ball: BallAssignment) -> str:
        """Place a single order"""

        is_buy = True if ball.position == BallType.LONG else False
        sz = (10 + 0.3) / ball.target_price
        payload = {
            "coin": self.coin,
            "is_buy": is_buy,
            "sz": sz,
            "px": ball.target_price,
            "is_market": False,
        }
        oid = "0"
        try:
            resp = await self.async_hyper.place_order(**payload)
            oid = parse_order_info(resp)
        except Exception as e:
            print(f"Order placement failed: {e}")

        ball.order_id = oid

        return oid

    async def cancel_orders(self, order_ids: List[str]) -> bool:
        """
        Cancel multiple orders
        """
        cancels = [(self.coin, int(oid)) for oid in order_ids]
        try:
            resp = await self.async_hyper.cancel_orders(cancels)
            print(f"Cancel response: {resp}")
        except Exception as e:
            print(f"Order cancellation failed: {e}")
            return False

        print(f"Cancelled {len(order_ids)} orders")
        return True

    async def monitor_order_fills(self, order_ids: List[str]) -> Optional[str]:
        """
        Monitor order fills via Hyperliquid WebSocket
        """
        filled_oid = None
        # WS_URL = "wss://api.hyperliquid.xyz/ws"
        WS_URL = "wss://api.hyperliquid-testnet.xyz/ws"
        async with websockets.connect(WS_URL) as ws:
            sub_msg = {
                "method": "subscribe",
                "subscription": {
                    "type": "order_fills",
                    "user": self.async_hyper.address,
                },
            }
            await ws.send(json.dumps(sub_msg))
            while True:
                ws_msg = await ws.recv()
                print(f"WebSocket message: {ws_msg}")

                msg = json.loads(ws_msg)
                channel = msg["channel"]
                data = msg["data"]
                if data.get("isSnapshot"):
                    continue
                if channel == "order_fills":
                    oid = data["fills"][0]["oid"]
                    filled_oid = oid
                    print(f"Order filled: {oid}")
                    break

        return filled_oid
