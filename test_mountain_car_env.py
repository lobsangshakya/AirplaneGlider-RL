#!/usr/bin/env python3
"""
Test script for Mountain Car-style Plane Glider environment
"""

import sys
import os

# Add the parent directory to the path to import env module
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from env.mountain_car_plane_env import MountainCarPlaneEnv
import numpy as np

def main():
    print("🧪 Testing Mountain Car-style Plane Glider Environment")
    print("=" * 55)
    
    # Create environment
    print("Creating environment...")
    env = MountainCarPlaneEnv()
    
    # Test reset
    print("Testing reset...")
    obs, info = env.reset()
    print(f"Initial observation: {obs}")
    print(f"Observation shape: {obs.shape}")
    
    # Test step
    print("\nTesting step...")
    action = 1  # No thrust
    obs, reward, done, truncated, info = env.step(action)
    print(f"After action {action}:")
    print(f"  Observation: {obs}")
    print(f"  Reward: {reward}")
    print(f"  Done: {done}")
    print(f"  Truncated: {truncated}")
    
    # Test all actions
    print("\nTesting all actions...")
    for action in range(3):
        obs, reward, done, truncated, info = env.step(action)
        print(f"Action {action}: Reward={reward:.2f}, Position=({obs[0]:.1f},{obs[1]:.1f}), Velocity=({obs[2]:.3f},{obs[3]:.3f})")
        if done:
            print("  Episode ended!")
            break
    
    # Test multiple steps
    print("\nTesting multiple steps...")
    env.reset()
    total_reward = 0
    for i in range(10):
        # Random action
        action = np.random.choice([0, 1, 2])
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        print(f"Step {i+1}: Action={action}, Reward={reward:.2f}, Total={total_reward:.2f}")
        if done:
            print(f"  Episode finished after {i+1} steps")
            break
    
    print("\n✅ Environment test completed successfully!")

if __name__ == "__main__":
    main()