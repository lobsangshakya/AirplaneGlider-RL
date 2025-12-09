#!/usr/bin/env python3
"""
Launcher script for Mountain Car-style Airplane Glider Game
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import stable_baselines3
        import numpy
        import gymnasium
        print("✓ All dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install fastapi uvicorn stable-baselines3 numpy gymnasium")
        return False

def main():
    """Main function to run the game"""
    print("🚀 Mountain Car Airplane Glider Game Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if model exists
    model_paths = [
        "models/mountain_car_plane_dqn_model.zip",
        "models/plane_dqn_model.zip"
    ]
    
    model_found = False
    for path in model_paths:
        if os.path.exists(path):
            print(f"✓ Found model: {path}")
            model_found = True
            break
    
    if not model_found:
        print("⚠️  Warning: No model file found!")
        print("   The AI control feature will not be available.")
        print("   You can still play with manual controls.")
        print("   Consider training a model with:")
        print("   cd training && python train_mountain_car.py")
        print()
    
    # Start the game server
    print("🎮 Starting Mountain Car Airplane Glider Game...")
    print("   Access the game at: http://localhost:8003")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the main application
        subprocess.run([
            sys.executable, 
            "airplane_glider_mountain_car.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running the game: {e}")

if __name__ == "__main__":
    main()