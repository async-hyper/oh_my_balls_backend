import asyncio
import os
import random
import uuid
from datetime import datetime
from typing import Dict, Optional

import dotenv
from async_hyper import AsyncHyper

from models.game import GameState, GameStatus
from services.ball_calculator import BallCalculator
from services.order_executor import OrderExecutor
from services.price_service import PriceService

dotenv.load_dotenv()


class GameManager:
    """Manages game state and lifecycle"""

    def __init__(self):
        self.current_game: Optional[GameState] = None
        self.ball_calculator = BallCalculator()

        address = os.getenv("HL_ADDR", "")
        pk = os.getenv("HL_PK", "")
        is_mainnet = os.getenv("IS_MAINNET", "true").lower() == "true"
        async_hyper = AsyncHyper(address, pk, is_mainnet)

        self.price_service = PriceService(async_hyper)
        self.order_executor = OrderExecutor(async_hyper)
        self._price_update_task: Optional[asyncio.Task] = None

    async def create_new_game(self) -> str:
        """Create a new game instance"""
        game_id = str(uuid.uuid4())
        self.current_game = GameState(game_id=game_id, status=GameStatus.PREPARING)
        return game_id

    async def join_game(self, participant_uuid: str) -> str:
        """Register a participant and assign a ball"""
        if not self.current_game:
            await self.create_new_game()

        if self.current_game.status != GameStatus.PREPARING:
            raise ValueError("Game is not in preparing state")

        if len(self.current_game.participants) >= 20:
            raise ValueError("Game is full")

        if participant_uuid in self.current_game.participants:
            raise ValueError("Participant already joined")

        # Generate ball assignments without prices if not done yet
        if not self.current_game.balls:
            self.current_game.balls = (
                self.ball_calculator.generate_empty_ball_assignments()
            )

        # Find next available ball
        available_balls = [ball for ball in self.current_game.balls if not ball.uuid]
        if not available_balls:
            raise ValueError("No balls available")

        assigned_ball = available_balls[0]
        assigned_ball.uuid = participant_uuid

        self.current_game.participants[participant_uuid] = assigned_ball.ball_name

        # Check if game is ready to start
        if len(self.current_game.participants) == 20:
            await self.start_game()

        return assigned_ball.ball_name

    async def start_game(self):
        """Start the game (transition from preparing to drawing)"""
        if not self.current_game or self.current_game.status != GameStatus.PREPARING:
            raise ValueError("Game not ready to start")

        # Get current BTC price and calculate ball prices
        self.current_game.initial_price = await self.price_service.get_current_price()
        self.ball_calculator.calculate_ball_prices(
            self.current_game.balls, self.current_game.initial_price
        )

        self.current_game.status = GameStatus.DRAWING
        self.current_game.start_time = datetime.now()

        # Start price update loop
        self._price_update_task = asyncio.create_task(self._price_update_loop())

        # Schedule order execution after 30 seconds
        asyncio.create_task(self._schedule_order_execution())

    async def _price_update_loop(self):
        """Update price every 100ms during active game"""
        while self.current_game and self.current_game.status == GameStatus.DRAWING:
            try:
                self.current_game.current_price = (
                    await self.price_service.get_current_price()
                )
                await asyncio.sleep(1)  # 1s
            except Exception as e:
                print(f"Price update error: {e}")
                await asyncio.sleep(1)

    async def _schedule_order_execution(self):
        """Schedule order execution after 30 seconds"""
        await asyncio.sleep(30)  # Wait 30 seconds

        if self.current_game and self.current_game.status == GameStatus.DRAWING:
            await self.execute_orders()

    async def execute_orders(self):
        """Execute all 20 orders and determine winner"""
        if not self.current_game:
            return

        try:
            # Place all orders using async-hyperliquid
            placed_orders = await self.order_executor.place_orders(
                self.current_game.balls
            )
            self.current_game.placed_orders = placed_orders

            # Monitor for first fill
            winner_ball = await self._monitor_order_fills()

            if winner_ball:
                self.current_game.winner = winner_ball
                self.current_game.status = GameStatus.DONE
                self.current_game.end_time = datetime.now()
                self.current_game.final_price = self.current_game.current_price

                # Stop price updates
                if self._price_update_task:
                    self._price_update_task.cancel()

        except Exception as e:
            print(f"Order execution error: {e}")
            self.current_game.status = GameStatus.DONE

    async def _monitor_order_fills(self) -> Optional[str]:
        """Monitor order fills via Hyperliquid WebSocket"""
        if not self.current_game.placed_orders:
            return None
        
        # Use real order monitoring
        filled_order_id = await self.order_executor.monitor_order_fills(
            self.current_game.placed_orders
        )
        
        if filled_order_id:
            # Find corresponding ball by order ID
            for ball in self.current_game.balls:
                if ball.order_id == filled_order_id:
                    return ball.ball_name
        
        return None

    def get_game_status(self, participant_uuid: str) -> Optional[Dict]:
        """Get current game status for a participant"""
        if not self.current_game:
            return None

        if participant_uuid not in self.current_game.participants:
            return None

        return {
            "status": self.current_game.status,
            "realtime_price": self.current_game.current_price or 0.0,
            "final_price": self.current_game.final_price or 0.0,
            "balls": [
                {
                    "ball_name": ball.ball_name,
                    "target_price": ball.target_price,
                    "uuid": ball.uuid,
                }
                for ball in self.current_game.balls
                if ball.uuid and ball.uuid.strip()  # Only show assigned balls
            ],
            "winner": self.current_game.winner or "",
        }

    def get_current_game(self) -> Optional[GameState]:
        """Get current game state"""
        return self.current_game

    async def force_start_game(self) -> Dict:
        """Force start game by auto-generating missing participants"""
        if not self.current_game:
            await self.create_new_game()

        if self.current_game.status != GameStatus.PREPARING:
            raise ValueError("Game is not in preparing state")

        current_participants = len(self.current_game.participants)
        missing_participants = 20 - current_participants

        if missing_participants <= 0:
            raise ValueError("Game already has 20 participants")

        # Generate ball assignments without prices if not done yet
        if not self.current_game.balls:
            self.current_game.balls = (
                self.ball_calculator.generate_empty_ball_assignments()
            )

        # Auto-generate missing participants
        auto_generated = []
        for i in range(missing_participants):
            auto_uuid = f"auto-participant-{i + 1:02d}"

            # Find next available ball
            available_balls = [
                ball for ball in self.current_game.balls if not ball.uuid
            ]
            if available_balls:
                assigned_ball = available_balls[0]
                assigned_ball.uuid = auto_uuid
                self.current_game.participants[auto_uuid] = assigned_ball.ball_name
                auto_generated.append(
                    {"uuid": auto_uuid, "ball": assigned_ball.ball_name}
                )

        # Start the game
        await self.start_game()

        return {
            "message": f"Game started with {missing_participants} auto-generated participants",
            "auto_generated": auto_generated,
            "total_participants": len(self.current_game.participants),
            "status": self.current_game.status,
        }

    def reset_game(self):
        """Reset game state for testing"""
        self.current_game = None
        if self._price_update_task:
            self._price_update_task.cancel()
            self._price_update_task = None
