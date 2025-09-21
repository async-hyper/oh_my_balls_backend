#!/usr/bin/env python3
"""
Demo script for the debug game
Shows how the debugger works with automatic participant addition
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000/api/v1"

def demo_debug():
    """Demo the debug functionality"""
    print("🎮 BTC Price Prediction Game - Debug Demo")
    print("=" * 50)
    
    # Reset game first
    print("🔄 Resetting game state...")
    try:
        response = requests.post(f"{BASE_URL}/game/reset")
        if response.status_code == 200:
            print("✅ Game reset successfully")
        else:
            print(f"⚠️  Game reset failed: {response.status_code}")
    except:
        print("⚠️  Game reset endpoint not available, continuing...")
    
    # Add participants automatically
    print("\n📝 Adding participants automatically...")
    participants = []
    
    for i in range(20):
        time.sleep(2)
        uuid = f"demo-player-{i+1:02d}"
        try:
            response = requests.post(f"{BASE_URL}/join", json={"uuid": uuid})
            if response.status_code == 200:
                ball = response.json()["ball"]
                participants.append({"uuid": uuid, "ball": ball})
                print(f"✅ Player {i+1:2d}: {uuid} -> {ball}")
                
                # Print complete status after each participant joins
                print(f"📊 Complete Status after adding {uuid}:")
                status_response = requests.get(f"{BASE_URL}/status", params={"uuid": uuid})
                if status_response.status_code == 200:
                    status = status_response.json()
                    
                    # Print complete JSON response as defined in API_Design.md
                    print("   📋 Full Status Response:")
                    print(f"   {json.dumps(status, indent=6)}")
                    
                    # Print summary
                    print(f"   📊 Summary: Status={status['status']} | Price=${status['realtime_price']:.2f} | Balls={len(status['balls'])}")
                    if status['status'] == 1:
                        print("   🎮 Game started! Orders will be executed in 30 seconds...")
                    elif status['status'] == 2:
                        print(f"   🏆 Game completed! Winner: {status['winner']}")
                else:
                    print(f"   ❌ Status check failed: {status_response.status_code}")
                print()
            else:
                print(f"❌ Player {i+1:2d} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Player {i+1:2d} error: {e}")
    
    print(f"\n📊 Added {len(participants)} participants")

    if len(participants) >= 20:
        print("\n🎉 Game should start automatically!")
        print("🔍 Monitoring game progress...")
        
        
        # Monitor the first participant
        monitor_uuid = participants[0]["uuid"]
        
        for i in range(10):  # Monitor for up to 30 iterations
            try:
                response = requests.get(f"{BASE_URL}/status", params={"uuid": monitor_uuid})
                if response.status_code == 200:
                    status = response.json()
                    print(f"\n🔄 Status {i+1:2d}: {status['status']} | Price: ${status['realtime_price']:.2f} | Balls: {len(status['balls'])}")
                    
                    if status['status'] == 1:
                        print("🎮 Game is in progress! Orders will be executed...")
                    elif status['status'] == 2:
                        print(f"🏆 Game completed! Winner: {status['winner']}")
                        print(f"📈 Final price: ${status['final_price']:.2f}")
                        break
                else:
                    print(f"❌ Status check failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Status error: {e}")
            
            time.sleep(2)
    
    print("\n🎯 Demo completed!")
    print("💡 You can now run: python debug_game.py")
    print("   This will start the interactive debugger where you can manually add UUIDs")

if __name__ == "__main__":
    demo_debug()
