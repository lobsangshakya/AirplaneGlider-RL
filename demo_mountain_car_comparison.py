#!/usr/bin/env python3
"""
Demonstration script comparing Mountain Car-style Plane Glider to classic Mountain Car
"""

import sys
import os

# Add the parent directory to the path to import env module
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from env.mountain_car_plane_env import MountainCarPlaneEnv
import numpy as np

def demonstrate_physics():
    """Demonstrate the physics differences between traditional and Mountain Car-style approaches"""
    
    print("🏔️  Mountain Car Physics Comparison")
    print("=" * 40)
    
    print("\n📋 Traditional Airplane Control:")
    print("  • Discrete position changes")
    print("  • Instant movement on key press")
    print("  • No momentum or velocity")
    print("  • Simple collision detection")
    
    print("\n🚗 Mountain Car-Style Physics:")
    print("  • Continuous position and velocity")
    print("  • Momentum-based movement")
    print("  • Gravity affects descent")
    print("  • Thrust affects acceleration")
    print("  • Realistic collision physics")
    
    print("\n📊 Key Differences:")
    print("  Traditional: Position = Position + Δ")
    print("  Mountain Car: Velocity = Velocity + Force")
    print("                Position = Position + Velocity")

def demonstrate_state_space():
    """Show the difference in state space representation"""
    
    print("\n🧮 State Space Comparison")
    print("=" * 30)
    
    print("\nTraditional Environment:")
    print("  Observations: [plane_x, plane_y, wind_x, time_remaining]")
    print("  Dimensions: 4")
    print("  Example: [200, 550, 150, 10.0]")
    
    print("\nMountain Car Environment:")
    print("  Observations: [plane_x, plane_y, velocity_x, velocity_y, wind_x, time_remaining]")
    print("  Dimensions: 6")
    print("  Example: [200.0, 550.0, 0.0, -0.05, 150.0, 10.0]")

def demonstrate_actions():
    """Show the action space differences"""
    
    print("\n🎮 Action Space Comparison")
    print("=" * 28)
    
    print("\nTraditional Actions:")
    print("  0: Move Left (Δx = -10)")
    print("  1: Stay (No movement)")
    print("  2: Move Right (Δx = +10)")
    
    print("\nMountain Car Actions:")
    print("  0: Left Thrust (Δvx = -0.03)")
    print("  1: No Thrust (vx remains)")
    print("  2: Right Thrust (Δvx = +0.03)")
    print("\n  Note: vy is affected by gravity (-0.05 per step)")

def run_simulation():
    """Run a simple simulation to show the physics in action"""
    
    print("\n🚀 Simulation Demo")
    print("=" * 18)
    
    # Create environment
    env = MountainCarPlaneEnv()
    obs, _ = env.reset()
    
    print(f"Initial State:")
    print(f"  Position: ({obs[0]:.1f}, {obs[1]:.1f})")
    print(f"  Velocity: ({obs[2]:.3f}, {obs[3]:.3f})")
    print(f"  Wind: ({obs[4]:.1f}, ?)")
    print(f"  Time: {obs[5]:.1f}s")
    
    print("\nApplying Right Thrust (Action 2) for 5 steps:")
    for i in range(5):
        obs, reward, done, truncated, _ = env.step(2)  # Right thrust
        print(f"Step {i+1}: Pos=({obs[0]:.1f},{obs[1]:.1f}) Vel=({obs[2]:.3f},{obs[3]:.3f}) Rew={reward:.2f}")
        if done:
            break
    
    print("\nCoasting (Action 1) for 5 steps:")
    for i in range(5):
        obs, reward, done, truncated, _ = env.step(1)  # No thrust
        print(f"Step {i+1}: Pos=({obs[0]:.1f},{obs[1]:.1f}) Vel=({obs[2]:.3f},{obs[3]:.3f}) Rew={reward:.2f}")
        if done:
            break

def main():
    print("🏔️  Mountain Car-Style Airplane Glider Demo")
    print("=" * 45)
    
    demonstrate_physics()
    demonstrate_state_space()
    demonstrate_actions()
    run_simulation()
    
    print("\n🎯 Benefits of Mountain Car Approach:")
    print("  • More realistic physics simulation")
    print("  • Better training for RL agents")
    print("  • More challenging and engaging gameplay")
    print("  • Closer to real-world flight dynamics")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()