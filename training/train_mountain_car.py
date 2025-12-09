#!/usr/bin/env python3
"""
Training script for Mountain Car-style Plane Glider environment
"""

import sys
import os

# Add the parent directory to the path to import env module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from stable_baselines3 import DQN
from env.mountain_car_plane_env import MountainCarPlaneEnv

def main():
    print("🚀 Training Mountain Car-style Plane Glider...")
    print("=" * 50)
    
    # Create environment
    print("Creating environment...")
    env = MountainCarPlaneEnv()
    
    # Create model
    print("Creating DQN model...")
    model = DQN(
        "MlpPolicy", 
        env, 
        verbose=1,
        learning_rate=1e-3,
        buffer_size=50000,
        learning_starts=1000,
        batch_size=32,
        tau=1.0,
        gamma=0.99,
        train_freq=4,
        gradient_steps=1,
        target_update_interval=1000,
        exploration_fraction=0.1,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,
        max_grad_norm=10
        # Removed tensorboard_log parameter since tensorboard is not installed
    )
    
    # Train model
    print("Starting training...")
    print("Training for 50,000 timesteps...")
    model.learn(total_timesteps=50000)
    
    # Save model
    model_save_path = "../models/mountain_car_plane_dqn_model"
    print(f"Saving model to {model_save_path}.zip...")
    model.save(model_save_path)
    print("✅ Model saved successfully!")
    
    # Test the trained model
    print("\n🧪 Testing trained model...")
    obs, _ = env.reset()
    total_reward = 0
    step_count = 0
    
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        step_count += 1
        
        if done or truncated:
            print(f"Episode finished after {step_count} timesteps")
            print(f"Total reward: {total_reward:.2f}")
            break
    
    print("\n🎉 Training completed!")
    print(f"Model saved as: {model_save_path}.zip")

if __name__ == "__main__":
    main()