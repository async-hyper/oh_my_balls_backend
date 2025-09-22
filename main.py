from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as api_router

app = FastAPI(
    title="Oh My Balls API",
    description="A BTC price prediction game for hackathon demonstration",
    version="1.0.0"
)

# Add CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Oh My Balls API",
        "version": "1.0.0",
        "endpoints": {
            "join": "POST /api/v1/join",
            "status": "GET /api/v1/status",
            "game_info": "GET /api/v1/game/info",
            "start": "GET /api/v1/start",
            "game_reset": "GET /api/v1/reset"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "btc_balls_game_api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
