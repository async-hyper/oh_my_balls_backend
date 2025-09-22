import asyncio
import json
from typing import List, Optional

import websockets
from async_hyper import AsyncHyper
from async_hyper.utils.types import LimitOrder

from models.ball import BallAssignment, BallType


def parse_order_info(resp: dict) -> str:
    return str(resp["response"]["data"]["statuses"][0]["resting"]["oid"])
    


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

        try:
            print(f"🌐 [NETWORK] Getting market price for {self.coin}...")
            mark_px = await self.async_hyper.get_market_price(self.coin)
            print(f"✅ [NETWORK] Market price retrieved: {mark_px}")
        except Exception as e:
            print(f"❌ [NETWORK] Failed to get market price: {type(e).__name__}: {e}")
            raise

        tasks = []
        for ball in balls:
            ball_name = ball.ball_name
            ball.position = (
                BallType.LONG if ball_name.startswith("B") else BallType.SHORT
            )

            offset = (int(ball_name[-1:]) + 1) * 1
            if ball.position == BallType.LONG:
                ball.target_price = mark_px - offset
            else:
                ball.target_price = mark_px + offset

            task = asyncio.create_task(self._place_single_order(ball))
            tasks.append(task)

        # Wait for all orders to be placed
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if result:  # 确保不为空
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
            "order_type": LimitOrder.ALO.value,
        }
        oid = ""
        try:
            print(f"🌐 [NETWORK] Placing order for {ball.ball_name}...")
            resp = await self.async_hyper.place_order(**payload)
            print(f"✅ [NETWORK] Order placed successfully for {ball.ball_name}")
            oid = parse_order_info(resp)
        except Exception as e:
            print(f"❌ [NETWORK] Order placement failed for {ball.ball_name}: {type(e).__name__}: {e}")
            # 如果异常包含order ID信息，尝试提取
            if isinstance(e, dict) and 'oid' in e:
                oid = str(e['oid'])
                print(f"🔄 [NETWORK] Extracted order ID from exception: {oid}")
            else:
                oid = ""  # 真正的失败，返回空字符串
                print(f"❌ [NETWORK] No order ID found in exception")

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
        
        try:
            print(f"🌐 [NETWORK] Connecting to WebSocket: {WS_URL}")
            print(f"📋 [NETWORK] Monitoring {len(order_ids)} orders: {order_ids}")
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ [NETWORK] WebSocket connected successfully")
                sub_msg = {
                    "method": "subscribe",
                    "subscription": {
                        "type": "order_fills",
                        "user": self.async_hyper.address,
                    },
                }
                print(f"📤 [NETWORK] Sending subscription message: {sub_msg}")
                await ws.send(json.dumps(sub_msg))
                print(f"✅ [NETWORK] Subscription message sent")
                
                message_count = 0
                while True:
                    try:
                        print(f"⏳ [NETWORK] Waiting for WebSocket message #{message_count + 1}...")
                        ws_msg = await ws.recv()
                        message_count += 1
                        print(f"📨 [NETWORK] WebSocket message #{message_count}: {ws_msg}")

                        msg = json.loads(ws_msg)
                        channel = msg.get("channel", "unknown")
                        data = msg.get("data", {})
                        
                        print(f"📊 [NETWORK] Channel: {channel}, Data keys: {list(data.keys())}")
                        
                        if data.get("isSnapshot"):
                            print(f"📸 [NETWORK] Snapshot message, skipping...")
                            continue
                        if channel == "order_fills":
                            fills = data.get("fills", [])
                            if fills:
                                oid = str(fills[0]["oid"])  # 确保是字符串格式
                                filled_oid = oid
                                print(f"🎉 [NETWORK] Order filled: {oid}")
                                break
                            else:
                                print(f"⚠️ [NETWORK] Order fills message but no fills data")
                        else:
                            print(f"ℹ️ [NETWORK] Other channel message: {channel}")
                    except Exception as e:
                        print(f"❌ [NETWORK] Error processing WebSocket message: {type(e).__name__}: {e}")
                        break
                        
        except Exception as e:
            print(f"❌ [NETWORK] WebSocket connection failed: {type(e).__name__}: {e}")
            print(f"🔍 [NETWORK] Error details: {str(e)}")
            return None

        return filled_oid
