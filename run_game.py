#!/usr/bin/env python3
"""
Launcher script for Airplane Glider Game
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import stable_baselines3
        import numpy
        print("✓ All dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install fastapi uvicorn stable-baselines3 numpy")
        return False

def main():
    """Main function to run the game"""
    print("🚀 Airplane Glider Game Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if model exists
    if not os.path.exists("models/plane_dqn_model.zip"):
        print("⚠️  Warning: Model file not found!")
        print("   The AI control feature will not be available.")
        print("   You can still play with manual controls.")
        print()
    
    # Start the game server
    print("🎮 Starting Airplane Glider Game...")
    print("   Access the game at: http://localhost:8000")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the main application
        subprocess.run([
            sys.executable, 
            "airplane_glider_app.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running the game: {e}")

if __name__ == "__main__":
    main()