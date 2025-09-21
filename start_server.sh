#!/bin/bash

# Start the BTC Price Prediction Game API server

echo "🚀 Starting BTC Price Prediction Game API Server..."
echo "================================================"

# Activate virtual environment
source venv/bin/activate

# Check if server is already running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  Server is already running on http://localhost:8000"
    echo "   You can test it with: python test_game.py"
    exit 0
fi

# Start the server
echo "📡 Starting server on http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py


