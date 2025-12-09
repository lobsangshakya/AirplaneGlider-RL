#!/usr/bin/env python3
"""
Launcher script for 2D Airplane Landing Simulator
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        print("✓ All dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install fastapi uvicorn")
        return False

def main():
    """Main function to run the landing simulator"""
    print("🚀 2D Airplane Landing Simulator Launcher")
    print("=" * 45)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the game server
    print("🎮 Starting 2D Airplane Landing Simulator...")
    print("   Access the game at: http://localhost:8004")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the main application
        subprocess.run([
            sys.executable, 
            "airplane_landing_simulator.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running the simulator: {e}")

if __name__ == "__main__":
    main()