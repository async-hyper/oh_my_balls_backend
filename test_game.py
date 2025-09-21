#!/usr/bin/env python3
"""
Test script for BTC Price Prediction Game API
"""
import asyncio
import json
import requests
import time
from typing import List

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🚀 Starting BTC Price Prediction Game API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Join game with multiple participants
    print("\n2. Testing join game...")
    participants = []
    for i in range(5):  # Test with 5 participants
        try:
            uuid = f"test-uuid-{i+1}"
            response = requests.post(
                f"{BASE_URL}/join",
                json={"uuid": uuid}
            )
            if response.status_code == 200:
                ball = response.json()["ball"]
                participants.append({"uuid": uuid, "ball": ball})
                print(f"✅ Participant {i+1}: {uuid} -> {ball}")
            else:
                print(f"❌ Participant {i+1} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Participant {i+1} error: {e}")
    
    # Test 3: Check game status
    print("\n3. Testing game status...")
    for participant in participants:
        try:
            response = requests.get(
                f"{BASE_URL}/status",
                params={"uuid": participant["uuid"]}
            )
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Status for {participant['uuid']}: status={status['status']}, price={status['realtime_price']}")
            else:
                print(f"❌ Status failed for {participant['uuid']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Status error for {participant['uuid']}: {e}")
    
    # Test 4: Game info
    print("\n4. Testing game info...")
    try:
        response = requests.get(f"{BASE_URL}/game/info")
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Game info: {json.dumps(info, indent=2)}")
        else:
            print(f"❌ Game info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Game info error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API tests completed!")

def test_full_game_simulation():
    """Simulate a full game with 20 participants"""
    print("\n🎮 Starting full game simulation...")
    print("=" * 50)
    
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
                print(f"❌ Player {i+1:2d} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Player {i+1:2d} error: {e}")
    
    print(f"\n📊 Registered {len(participants)} participants")
    
    # Monitor game status
    print("\n⏱️  Monitoring game status...")
    for i in range(10):  # Monitor for 10 iterations
        try:
            # Check status for first participant
            response = requests.get(
                f"{BASE_URL}/status",
                params={"uuid": participants[0]["uuid"]}
            )
            if response.status_code == 200:
                status = response.json()
                print(f"🔄 Status {i+1}: status={status['status']}, price={status['realtime_price']:.2f}")
                
                if status['status'] == 2:  # Game done
                    print(f"🏆 Game completed! Winner: {status['winner']}")
                    break
            else:
                print(f"❌ Status check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Status check error: {e}")
        
        time.sleep(1)  # Wait 1 second between checks
    
    print("\n🎉 Full game simulation completed!")

if __name__ == "__main__":
    print("Make sure the server is running on http://localhost:8000")
    print("You can start it with: python main.py")
    print()
    
    # Run basic API tests
    test_api_endpoints()
    
    # Uncomment to run full game simulation
    # test_full_game_simulation()
