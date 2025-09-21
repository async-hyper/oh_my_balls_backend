#!/usr/bin/env python3
"""
Full game simulation test for BTC Price Prediction Game API
"""
import asyncio
import json
import requests
import time
from typing import List

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_full_game_simulation():
    """Simulate a full game with 20 participants"""
    print("🎮 Starting Full Game Simulation")
    print("=" * 50)
    
    # Reset game state first
    print("🔄 Resetting game state...")
    try:
        response = requests.post(f"{BASE_URL}/game/reset")
        if response.status_code == 200:
            print("✅ Game reset successfully")
        else:
            print(f"❌ Game reset failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Game reset error: {e}")
    
    participants = []
    
    # Register 20 participants
    print("\n📝 Registering 20 participants...")
    for i in range(20):
        try:
            uuid = f"player-{i+1:02d}"
            response = requests.post(
                f"{BASE_URL}/join",
                json={"uuid": uuid}
            )
            if response.status_code == 200:
                ball = response.json()["ball"]
                participants.append({"uuid": uuid, "ball": ball})
                print(f"✅ Player {i+1:2d}: {uuid} -> {ball}")
            else:
                print(f"❌ Player {i+1:2d} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Player {i+1:2d} error: {e}")
    
    print(f"\n📊 Registered {len(participants)} participants")
    
    if len(participants) < 20:
        print("❌ Not enough participants to start game")
        return
    
    # Monitor game status
    print("\n⏱️  Monitoring game status...")
    print("Game should start automatically with 20 participants...")
    
    for i in range(50):  # Monitor for up to 50 iterations (50 seconds)
        try:
            # Check status for first participant
            response = requests.get(
                f"{BASE_URL}/status",
                params={"uuid": participants[0]["uuid"]}
            )
            if response.status_code == 200:
                status = response.json()
                print(f"🔄 Status {i+1:2d}: status={status['status']}, price={status['realtime_price']:.2f}, balls={len(status['balls'])}")
                
                if status['status'] == 1:  # Game started
                    print("🎯 Game started! Price updates every 100ms...")
                elif status['status'] == 2:  # Game done
                    print(f"🏆 Game completed! Winner: {status['winner']}")
                    print(f"📈 Final price: {status['final_price']:.2f}")
                    break
            else:
                print(f"❌ Status check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Status check error: {e}")
        
        time.sleep(1)  # Wait 1 second between checks
    
    # Show final results
    print("\n📋 Final Results:")
    try:
        response = requests.get(f"{BASE_URL}/game/info")
        if response.status_code == 200:
            info = response.json()
            print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"❌ Final results error: {e}")
    
    print("\n🎉 Full game simulation completed!")

def test_ball_distribution():
    """Test ball distribution (10 long, 10 short)"""
    print("\n🎯 Testing Ball Distribution")
    print("=" * 30)
    
    # Start fresh game
    participants = []
    for i in range(20):
        uuid = f"dist-test-{i+1:02d}"
        response = requests.post(f"{BASE_URL}/join", json={"uuid": uuid})
        if response.status_code == 200:
            ball = response.json()["ball"]
            participants.append(ball)
    
    # Count ball types
    long_balls = [ball for ball in participants if ball.startswith('B')]
    short_balls = [ball for ball in participants if ball.startswith('S')]
    
    print(f"📊 Long balls (B0-B9): {len(long_balls)} - {long_balls}")
    print(f"📊 Short balls (S0-S9): {len(short_balls)} - {short_balls}")
    
    if len(long_balls) == 10 and len(short_balls) == 10:
        print("✅ Ball distribution is correct!")
    else:
        print("❌ Ball distribution is incorrect!")

if __name__ == "__main__":
    print("Make sure the server is running on http://localhost:8000")
    print("You can start it with: python main.py")
    print()
    
    # Test ball distribution
    test_ball_distribution()
    
    # Run full game simulation
    test_full_game_simulation()
