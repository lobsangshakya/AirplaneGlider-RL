import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MountainCarPlaneEnv(gym.Env):
    """Custom Environment for Plane Glider with Mountain Car-style physics"""
    
    def __init__(self):
        super(MountainCarPlaneEnv, self).__init__()
        
        # Define action space: 0=left thrust, 1=no thrust, 2=right thrust
        self.action_space = spaces.Discrete(3)
        
        # Define observation space:
        # [plane_x, plane_y, velocity_x, velocity_y, wind_x, time_remaining]
        low = np.array([0.0, 0.0, -1.0, -1.0, 0.0, 0.0], dtype=np.float32)
        high = np.array([400.0, 600.0, 1.0, 1.0, 400.0, 15.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        
        # Physics constants
        self.gravity = 0.05
        self.thrust_power = 0.03
        self.wind_strength = 0.02
        
        # Initialize state
        self.reset()
    
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        
        # Reset plane to starting position (middle top)
        self.plane_x = 200.0
        self.plane_y = 550.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
        # Reset wind position
        self.wind_x = np.random.uniform(50, 350)
        self.wind_y = 0.0
        
        # Reset timer
        self.time_remaining = 15.0
        
        return self._get_obs(), {}
    
    def _get_obs(self):
        return np.array([
            self.plane_x,
            self.plane_y,
            self.velocity_x,
            self.velocity_y,
            self.wind_x,
            self.time_remaining
        ], dtype=np.float32)
    
    def step(self, action):
        # Apply physics based on action
        if action == 0:  # Left thrust
            self.velocity_x -= self.thrust_power
        elif action == 2:  # Right thrust
            self.velocity_x += self.thrust_power
        
        # Apply gravity (natural glide downward)
        self.velocity_y -= self.gravity
        
        # Update positions based on velocities
        self.plane_x += self.velocity_x
        self.plane_y += self.velocity_y
        
        # Apply wind effect (random horizontal push)
        if np.random.random() < 0.1:  # 10% chance each step
            wind_direction = np.random.choice([-1, 1])
            self.velocity_x += wind_direction * self.wind_strength
        
        # Boundary checks
        if self.plane_x < 0:
            self.plane_x = 0
            self.velocity_x = 0
        elif self.plane_x > 400:
            self.plane_x = 400
            self.velocity_x = 0
            
        if self.plane_y < 0:
            self.plane_y = 0
            self.velocity_y = 0
        elif self.plane_y > 600:
            self.plane_y = 600
            self.velocity_y = 0
        
        # Move wind downward
        self.wind_y += 2
        if self.wind_y > 600:
            self.wind_y = 0
            self.wind_x = np.random.uniform(50, 350)
        
        # Decrease timer
        self.time_remaining -= 0.1
        
        # Calculate reward and done
        done = False
        reward = 0
        
        # Collision detection
        if (abs(self.plane_x - self.wind_x) < 30 and 
            abs(self.plane_y - self.wind_y) < 30):
            reward = -10
            done = True
        else:
            # Reward for staying airborne
            reward = 1 + (self.plane_y / 600) * 0.5  # Higher reward for higher altitude
        
        # Time limit
        if self.time_remaining <= 0:
            reward += 5
            done = True
        
        truncated = False
        return self._get_obs(), reward, done, truncated, {}
    
    def render(self, mode='human'):
        print(f"Plane Pos:({self.plane_x:.1f},{self.plane_y:.1f}) "
              f"Vel:({self.velocity_x:.2f},{self.velocity_y:.2f}) "
              f"Wind:({self.wind_x:.1f},{self.wind_y:.1f}) "
              f"Time:{self.time_remaining:.1f}")