# Airplane Glider RL

A reinforcement learning-powered airplane glider game where players control an airplane to avoid wind obstacles. Features both traditional and Mountain Car-style physics simulations.

## 🏔️ Mountain Car Implementation

This implementation follows the physics-based approach of the classic Mountain Car problem, where the airplane has:
- **Position and Velocity**: Both horizontal and vertical velocity components
- **Physics Simulation**: Gravity, thrust, and momentum
- **Continuous State Space**: More realistic movement mechanics
- **Enhanced Challenge**: Requires building momentum to navigate effectively

Based on the reference notebook: https://github.com/lobsangshakya/reinforcement-learning/blob/master/FA/MountainCar%20Playground.ipynb

## 📁 Project Structure
```
AirplaneGlider-RL/
├── env/                          # Custom airplane environments (Gymnasium)
│   ├── env.py                    # Traditional environment
│   └── mountain_car_plane_env.py # Mountain Car-style physics environment
├── models/                       # Trained model files and weights
├── src/                          # Main Python backend logic (FastAPI)
├── training/                     # Training scripts for RL models
│   ├── train.py                  # Traditional training
│   └── train_mountain_car.py     # Mountain Car-style training
├── web/                          # HTML, CSS, JavaScript for game UI
├── airplane_glider_app.py        # Traditional game implementation
├── airplane_glider_mountain_car.py # Mountain Car-style implementation
├── run_game.py                   # Launcher for traditional game
├── run_mountain_car.py           # Launcher for Mountain Car game
├── main.py                       # FastAPI entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Games

### Traditional Version
#### 1. Start the Backend Server
```bash
python main.py
```
The backend will start on `http://127.0.0.1:8002`

#### 2. Start the Frontend Server
```bash
cd web
python -m http.server 8080
```

#### 3. Play the Game
Open your browser and navigate to `http://localhost:8080`

### Mountain Car-Style Version (Physics-based)
#### Option 1: Using the launcher script
```bash
python run_mountain_car.py
```

#### Option 2: Direct execution
```bash
python airplane_glider_mountain_car.py
```

The game will start on `http://localhost:8001`

## 🎮 How to Play

### Traditional Version
- **W** - Move Up (Forward)
- **S** - Move Down (Backward)
- **A** - Move Left
- **D** - Move Right

### Mountain Car-Style Version
- **←** - Left Thrust
- **↑** - Upward Thrust
- **→** - Right Thrust

Objective: Survive for 15 seconds without hitting the wind obstacles.

The Mountain Car version features physics-based movement with velocity and momentum, similar to the classic Mountain Car reinforcement learning problem.

## 🤖 Reinforcement Learning Models

### Traditional Model
This game uses a Deep Q-Network (DQN) trained with Stable Baselines3. The model was trained in the custom airplane environment defined in `env/env.py`.

#### Training Process
The model learns to:
1. Observe the plane's position
2. Track wind obstacle locations
3. Make decisions to move left, right, or stay in place
4. Maximize survival time

#### Environment Details
- **Actions**: 3 discrete actions (Left, Stay, Right)
- **Observations**: Plane X, Plane Y, Wind X, Time Remaining
- **Reward**: +1 for each timestep survived, -10 for collision

### Mountain Car-Style Model
Features physics-based movement with velocity and momentum, similar to the classic Mountain Car reinforcement learning problem.

#### Environment Details
- **Actions**: 3 discrete actions (Left Thrust, No Thrust, Right Thrust)
- **Observations**: Plane X, Plane Y, Velocity X, Velocity Y, Wind X, Time Remaining
- **Physics**: Gravity, thrust power, wind effects
- **Reward**: +1 for each timestep survived plus altitude bonus, -10 for collision

## 📂 Directory Explanation

- **env/env.py**: Traditional airplane environment
- **env/mountain_car_plane_env.py**: Mountain Car-style physics environment
- **models/**: Stores the trained DQN model weights
- **src/**: FastAPI backend that serves predictions to the frontend
- **training/train.py**: Script to train traditional model
- **training/train_mountain_car.py**: Script to train Mountain Car-style model
- **web/**: Frontend game interface (HTML/CSS/JS)
- **airplane_glider_app.py**: Traditional game implementation with embedded frontend
- **airplane_glider_mountain_car.py**: Mountain Car-style implementation with embedded frontend

## 🧪 Training New Models

### Traditional Model
To train the traditional model:
```bash
cd training
python train.py
```

This will save the trained model to `models/plane_dqn_model.zip`.

### Mountain Car-Style Model
To train the Mountain Car-style model:
```bash
cd training
python train_mountain_car.py
```

This will save the trained model to `models/mountain_car_plane_dqn_model.zip`.