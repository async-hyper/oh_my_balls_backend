from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from services.game_manager import GameManager

router = APIRouter()

# Initialize game manager
game_manager = GameManager()

class JoinRequest(BaseModel):
    uuid: str

class JoinResponse(BaseModel):
    ball: str

class StatusRequest(BaseModel):
    uuid: str

class StatusResponse(BaseModel):
    status: int
    realtime_price: float
    final_price: float
    balls: list
    winner: str
    p0: float
    t0: int

@router.post("/join", response_model=JoinResponse)
async def join_game(request: JoinRequest):
    """
    Register a participant and receive a ball assignment
    """
    try:
        # Ensure async components are initialized
        await game_manager._ensure_async_components()
        ball_name = await game_manager.join_game(request.uuid)
        return JoinResponse(ball=ball_name)
    
    except ValueError as e:
        if "Game is full" in str(e):
            raise HTTPException(status_code=409, detail="Game is full")
        else:
            raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/status", response_model=StatusResponse)
async def get_game_status():
    """
    Get current game status and real-time information
    """
    try:
        status_data = game_manager.get_game_status()
        return StatusResponse(**status_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/game/info")
async def get_game_info():
    """
    Get general game information (for debugging)
    """
    current_game = game_manager.get_current_game()
    
    if not current_game:
        return {"message": "No active game"}
    
    return {
        "game_id": current_game.game_id,
        "status": current_game.status,
        "participants_count": len(current_game.participants),
        "start_time": current_game.start_time,
        "initial_price": current_game.initial_price,
        "current_price": current_game.current_price
    }

@router.get("/start")
async def start_game():
    """
    Force start game by auto-generating missing participants
    """
    try:
        # Ensure async components are initialized
        await game_manager._ensure_async_components()
        result = await game_manager.force_start_game()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/reset")
async def reset_game():
    """
    Reset game state (for testing)
    """
    game_manager.reset_game()
    return {"message": "Game reset successfully"}
