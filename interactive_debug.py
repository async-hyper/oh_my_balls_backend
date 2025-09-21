#!/usr/bin/env python3
"""
Interactive Debug Script for BTC Price Prediction Game
- Reset all data and status on start
- Manual UUID input with real-time status display
- Auto-monitoring after 20 participants
- Automatic lottery draw when conditions are met
"""
import requests
import json
import time
import threading
import signal
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

class InteractiveGameDebugger:
    def __init__(self):
        self.participants = []
        self.monitoring = False
        self.game_completed = False
        self.monitor_thread = None
        
    def print_separator(self, title="", char="="):
        """Print a visual separator"""
        if title:
            print(f"\n{char*20} {title} {char*20}")
        else:
            print(char*60)
    
    def reset_all_data(self):
        """Reset all game data and status"""
        self.print_separator("RESETTING GAME DATA")
        print("🔄 Clearing all data and resetting game state...")
        
        try:
            response = requests.post(f"{BASE_URL}/game/reset")
            if response.status_code == 200:
                print("✅ Game reset successfully")
                self.participants = []
                self.monitoring = False
                self.game_completed = False
                return True
            else:
                print(f"⚠️  Game reset failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Reset error: {e}")
            return False
    
    def check_server_connection(self):
        """Check if server is running"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=3)
            if response.status_code == 200:
                print("✅ Server is running")
                return True
            else:
                print("❌ Server responded with error")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            print("Please start the server with: python main.py")
            return False
    
    def join_participant(self, uuid):
        """Add a participant and return status"""
        try:
            # Join the game
            response = requests.post(f"{BASE_URL}/join", json={"uuid": uuid})
            
            # Print join API response
            self.print_separator(f"JOIN API Response for {uuid}", "-")
            print(f"📡 Status Code: {response.status_code}")
            print(f"📋 Response Body: {response.text}")
            if response.status_code == 200:
                print(f"📊 Parsed JSON: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                ball = response.json()["ball"]
                self.participants.append({"uuid": uuid, "ball": ball})
                print(f"✅ {uuid} joined successfully! Assigned ball: {ball}")
                
                # Get and print status
                status_response = requests.get(f"{BASE_URL}/status", params={"uuid": uuid})
                if status_response.status_code == 200:
                    status = status_response.json()
                    self.print_status_json(status, f"Status after adding {uuid}")
                    return status
                else:
                    print(f"❌ Failed to get status: {status_response.status_code}")
                    return None
                    
            elif response.status_code == 409:
                if "already joined" in response.text:
                    print(f"⚠️  {uuid} has already joined the game")
                    # Still get status
                    status_response = requests.get(f"{BASE_URL}/status", params={"uuid": uuid})
                    if status_response.status_code == 200:
                        status = status_response.json()
                        self.print_status_json(status, f"Status for existing {uuid}")
                        return status
                elif "Game is full" in response.text:
                    print(f"❌ Game is full! Cannot join {uuid}")
                else:
                    print(f"❌ Join failed: {response.text}")
            else:
                print(f"❌ Join failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error joining participant: {e}")
        
        return None
    
    def print_status_json(self, status, title="Game Status"):
        """Print complete status JSON with formatting"""
        self.print_separator(title, "-")
        print("📋 Complete Status JSON:")
        print(json.dumps(status, indent=4))
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"   Status: {self.get_status_name(status['status'])}")
        print(f"   Real-time Price: ${status['realtime_price']:.2f}")
        print(f"   Final Price: ${status['final_price']:.2f}")
        print(f"   Assigned Balls: {len(status['balls'])}")
        print(f"   Winner: {status['winner'] or 'Not determined'}")
        
        if status['status'] == 1:
            print("   🎮 Game is in progress!")
        elif status['status'] == 2:
            print("   🏆 Game completed!")
    
    def get_status_name(self, status_code):
        """Convert status code to readable name"""
        status_names = {
            0: "PREPARING (waiting for 20 participants)",
            1: "DRAWING (game in progress)", 
            2: "COMPLETED (winner determined)"
        }
        return status_names.get(status_code, f"UNKNOWN ({status_code})")
    
    def start_auto_monitoring(self, monitor_uuid):
        """Start automatic monitoring after 20 participants"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(monitor_uuid,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor_loop(self, monitor_uuid):
        """Auto-monitoring loop - runs every 2 seconds"""
        print(f"\n🔍 Starting auto-monitoring for {monitor_uuid}...")
        print("📊 Will print status every 2 seconds until game completes")
        print("Press Ctrl+C to stop monitoring and return to manual input")
        
        iteration = 1
        while self.monitoring and not self.game_completed:
            try:
                response = requests.get(f"{BASE_URL}/status", params={"uuid": monitor_uuid})
                if response.status_code == 200:
                    status = response.json()
                    
                    self.print_separator(f"AUTO-MONITOR #{iteration} - {datetime.now().strftime('%H:%M:%S')}", "-")
                    print("📋 Complete Status JSON:")
                    print(json.dumps(status, indent=4))
                    
                    # Check if game completed
                    if status['status'] == 2:
                        self.game_completed = True
                        self.print_separator("🏆 LOTTERY DRAW COMPLETED!", "🎉")
                        print(f"🎊 Winner: {status['winner']}")
                        print(f"💰 Final Price: ${status['final_price']:.2f}")
                        print(f"📈 Real-time Price: ${status['realtime_price']:.2f}")
                        
                        # Find winner details
                        winner_ball = status['winner']
                        winner_participant = None
                        for p in self.participants:
                            if p['ball'] == winner_ball:
                                winner_participant = p
                                break
                        
                        if winner_participant:
                            print(f"🎯 Winner Details:")
                            print(f"   UUID: {winner_participant['uuid']}")
                            print(f"   Ball: {winner_participant['ball']}")
                        
                        self.monitoring = False
                        break
                    else:
                        print(f"\n📊 Summary: Status={self.get_status_name(status['status'])}, Price=${status['realtime_price']:.2f}")
                        if status['status'] == 1:
                            print("⏱️  Waiting for lottery draw...")
                
                else:
                    print(f"❌ Status check failed: {response.status_code}")
                
                iteration += 1
                time.sleep(2)  # Wait 2 seconds
                
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(2)
    
    def stop_monitoring(self):
        """Stop auto-monitoring"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
    
    def run_interactive_session(self):
        """Run the main interactive session"""
        self.print_separator("🎮 BTC PRICE PREDICTION GAME - INTERACTIVE DEBUGGER")
        print("🔧 Debug Features:")
        print("   • Auto-reset all data on start")
        print("   • Manual UUID input with real-time status")
        print("   • Auto-monitoring after 20 participants")
        print("   • Automatic lottery draw detection")
        print("   • Complete JSON status display")
        
        # Check server connection
        if not self.check_server_connection():
            return
        
        # Reset all data
        if not self.reset_all_data():
            return
        
        self.print_separator("📝 MANUAL PARTICIPANT INPUT")
        print("💡 Instructions:")
        print("   • Enter UUID to add participant")
        print("   • Type 'quit' to exit")
        print("   • Type 'status <uuid>' to check specific status")
        print("   • Game will auto-monitor after 20 participants")
        
        while True:
            try:
                if self.game_completed:
                    print("\n🎉 Game completed! Type 'quit' to exit or enter new UUID to start fresh.")
                
                command = input(f"\n🎯 Enter UUID (participants: {len(self.participants)}/20): ").strip()
                
                if command.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                    
                elif command.startswith('status '):
                    uuid = command[7:].strip()
                    if uuid:
                        response = requests.get(f"{BASE_URL}/status", params={"uuid": uuid})
                        if response.status_code == 200:
                            status = response.json()
                            self.print_status_json(status, f"Manual Status Check for {uuid}")
                        else:
                            print(f"❌ Status check failed: {response.status_code}")
                    else:
                        print("❌ Please provide a UUID")
                    continue
                    
                elif not command:
                    continue
                
                # Add participant
                status = self.join_participant(command)
                
                # Check if we reached 20 participants and game started
                if status and len(self.participants) >= 20 and status['status'] == 1:
                    print(f"\n🎉 Game started with 20 participants!")
                    print("🚀 Starting auto-monitoring mode...")
                    self.start_auto_monitoring(self.participants[0]['uuid'])
                
            except KeyboardInterrupt:
                if self.monitoring:
                    print(f"\n⏸️  Stopping auto-monitoring...")
                    self.stop_monitoring()
                    print("🔄 Returning to manual input mode")
                else:
                    print(f"\n👋 Goodbye!")
                    break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_monitoring()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n👋 Exiting...')
    sys.exit(0)

def main():
    """Main function"""
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Starting Interactive BTC Price Prediction Game Debugger")
    print("Make sure the server is running on http://localhost:8000")
    
    debugger = InteractiveGameDebugger()
    try:
        debugger.run_interactive_session()
    finally:
        debugger.cleanup()

if __name__ == "__main__":
    main()
