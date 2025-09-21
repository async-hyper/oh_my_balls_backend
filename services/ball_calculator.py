import random
from typing import List
from models.ball import BallAssignment, BallType

class BallCalculator:
    """Calculates target prices for balls based on initial BTC price"""
    
    def __init__(self):
        self.long_balls = [f"B{i}" for i in range(10)]  # B0-B9
        self.short_balls = [f"S{i}" for i in range(10)]  # S0-S9
    
    def generate_empty_ball_assignments(self) -> List[BallAssignment]:
        """Generate 20 ball assignments without prices (only ball names)"""
        balls = []
        
        # Create long balls (B0-B9) without prices
        for ball_name in self.long_balls:
            balls.append(BallAssignment(
                ball_name=ball_name,
                target_price=0.0,  # Will be set when game starts
                uuid="",  # Will be assigned when participant joins
                position=BallType.LONG
            ))
        
        # Create short balls (S0-S9) without prices
        for ball_name in self.short_balls:
            balls.append(BallAssignment(
                ball_name=ball_name,
                target_price=0.0,  # Will be set when game starts
                uuid="",  # Will be assigned when participant joins
                position=BallType.SHORT
            ))
        
        # Shuffle the balls to randomize assignment order
        random.shuffle(balls)
        return balls
    
    def calculate_ball_prices(self, balls: List[BallAssignment], initial_price: float):
        """Calculate target prices for balls with 2-point gap"""
        for ball in balls:
            if ball.ball_name.startswith('B'):
                # Long balls: B0=price+2, B1=price+4, B2=price+6, etc.
                ball_number = int(ball.ball_name[1:])  # Extract number from B0, B1, etc.
                ball.target_price = initial_price + (ball_number + 1) * 2
            elif ball.ball_name.startswith('S'):
                # Short balls: S0=price-2, S1=price-4, S2=price-6, etc.
                ball_number = int(ball.ball_name[1:])  # Extract number from S0, S1, etc.
                ball.target_price = initial_price - (ball_number + 1) * 2
    
    def find_ball_by_price(self, filled_price: float, balls: List[BallAssignment]) -> str:
        """Find the ball with the closest target price to the filled price"""
        if not balls:
            return None
        
        closest_ball = min(balls, key=lambda ball: abs(ball.target_price - filled_price))
        return closest_ball.ball_name
