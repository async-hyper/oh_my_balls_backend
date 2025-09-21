from fastapi import FastAPI

app = FastAPI(
    title="Balls Game API",
    description="A simple FastAPI backend for balls game",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint - Hello World"""
    return {"message": "Hello World! Welcome to Balls Game API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "balls_game_api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
