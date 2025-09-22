#!/usr/bin/env python3
"""
Test script to verify the new pricing logic
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_pricing_logic():
    """Test the new pricing logic with 20 participants"""
    print("🧪 Testing New Pricing Logic")
    print("=" * 50)
    
    # Reset game
    print("🔄 Resetting game...")
    try:
        response = requests.get(f"{BASE_URL}/reset")
        if response.status_code == 200:
            print("✅ Game reset successfully")
        else:
            print(f"⚠️  Game reset failed: {response.status_code}")
    except:
        print("⚠️  Game reset not available")
    
    # Add 20 participants
    print("\n📝 Adding 20 participants to trigger price calculation...")
    participants = []
    
    for i in range(20):
        uuid = f"test-player-{i+1:02d}"
        try:
            response = requests.post(f"{BASE_URL}/join", json={"uuid": uuid})
            if response.status_code == 200:
                ball = response.json()["ball"]
                participants.append({"uuid": uuid, "ball": ball})
                print(f"✅ Player {i+1:2d}: {uuid} -> {ball}")
                
                # Show status only for the last few participants to see the price calculation
                if i >= 18:  # Show for participants 19 and 20
                    status_response = requests.get(f"{BASE_URL}/status", params={"uuid": uuid})
                    if status_response.status_code == 200:
                        status = status_response.json()
                        print(f"   Status: {status['status']} | Balls with prices: {len([b for b in status['balls'] if b['target_price'] > 0])}")
            else:
                print(f"❌ Player {i+1:2d} failed: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ Player {i+1:2d} error: {e}")
            break
    
    print(f"\n📊 Added {len(participants)} participants")
    
    if len(participants) >= 20:
        print("\n🎯 Game should have started! Let's check the final pricing...")
        
        # Get final status to see all ball prices
        final_uuid = participants[0]["uuid"]
        response = requests.get(f"{BASE_URL}/status", params={"uuid": final_uuid})
        if response.status_code == 200:
            status = response.json()
            print(f"\n📈 Final Game Status:")
            print(f"   Status: {status['status']} (should be 1 - drawing)")
            latest_price = status.get('realtime_price', [])
            price_value = list(latest_price[-1].values())[0] if latest_price else 0
            print(f"   Initial Price: ${price_value:.2f}")
            print(f"   Total Balls: {len(status['balls'])}")
            
            # Sort and display balls by type and number
            balls = status['balls']
            long_balls = sorted([b for b in balls if b['ball_name'].startswith('B')], 
                              key=lambda x: int(x['ball_name'][1:]))
            short_balls = sorted([b for b in balls if b['ball_name'].startswith('S')], 
                               key=lambda x: int(x['ball_name'][1:]))
            
            # Get the initial price for comparison (balls are calculated based on initial price)
            game_info_response = requests.get(f"{BASE_URL}/game/info")
            initial_price = 0
            if game_info_response.status_code == 200:
                game_info = game_info_response.json()
                initial_price = game_info.get('initial_price', 0)
            
            latest_price = status.get('realtime_price', [])
            price_value = list(latest_price[-1].values())[0] if latest_price else 0
            print(f"   Real-time Price: ${price_value:.2f}")
            print(f"   Initial Price (for calculation): ${initial_price:.2f}")
            
            print(f"\n🟢 Long Balls (should be initial_price + 2*n):")
            for ball in long_balls:
                ball_num = int(ball['ball_name'][1:])
                expected = initial_price + (ball_num + 1) * 2
                actual = ball['target_price']
                match = "✅" if abs(expected - actual) < 0.01 else "❌"
                print(f"   {match} {ball['ball_name']}: ${actual:.2f} (expected: ${expected:.2f})")
            
            print(f"\n🔴 Short Balls (should be initial_price - 2*n):")
            for ball in short_balls:
                ball_num = int(ball['ball_name'][1:])
                expected = initial_price - (ball_num + 1) * 2
                actual = ball['target_price']
                match = "✅" if abs(expected - actual) < 0.01 else "❌"
                print(f"   {match} {ball['ball_name']}: ${actual:.2f} (expected: ${expected:.2f})")
        else:
            print(f"❌ Failed to get final status: {response.status_code}")
    
    print("\n🎯 Pricing test completed!")

if __name__ == "__main__":
    test_pricing_logic()
