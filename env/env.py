import gymnasium as gym
from gymnasium import spaces
import numpy as np

class PlaneGliderEnv(gym.Env):
    """Custom Environment for Plane Glider"""
    
    def __init__(self):
        super(PlaneGliderEnv, self).__init__()
        
        # Discrete actions: 0=left, 1=stay, 2=right
        self.action_space = spaces.Discrete(3)
        
        # Observations: plane_x, plane_y, wind_x, time_remaining
        high = np.array([400.0, 600.0, 400.0, 15.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([0,0,0,0]), high=high, dtype=np.float32)
        
        # Initial state
        self.reset()
    
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.plane_x = 200
        self.plane_y = 550
        self.wind_x = np.random.randint(50, 350)
        self.time_remaining = 15
        return self._get_obs(), {}
    
    def _get_obs(self):
        return np.array([self.plane_x, self.plane_y, self.wind_x, self.time_remaining], dtype=np.float32)
    
    def step(self, action):
        # Move plane
        if action == 0:
            self.plane_x -= 10
        elif action == 2:
            self.plane_x += 10
            
        # Glide down
        self.plane_y -= 5
        
        # Decrease timer
        self.time_remaining -= 0.1
        
        done = False
        reward = 0
        
        # Collision detection
        if abs(self.plane_x - self.wind_x) < 30 and self.plane_y < 600:
            reward = -10
            done = True
        else:
            reward = +1
        
        # End after 15 seconds
        if self.time_remaining <= 0:
            reward += 5
            done = True
        
        truncated = False
        return self._get_obs(), reward, done, truncated, {}
    
    def render(self, mode='human'):
        print(f"Plane X:{self.plane_x} Y:{self.plane_y} | Wind X:{self.wind_x} | Time:{round(self.time_remaining,1)}")