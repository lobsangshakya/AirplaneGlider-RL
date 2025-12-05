# Airplane Glider RL

A reinforcement learning-powered airplane glider game where players control an airplane to avoid wind obstacles.

## 📁 Project Structure

```
AirplaneGlider-RL/
├── env/               # Custom airplane environment (Gymnasium)
├── models/            # Trained model files and weights
├── src/               # Main Python backend logic (FastAPI)
├── training/          # Training scripts for RL model
├── web/               # HTML, CSS, JavaScript for game UI
├── config/            # Configuration files
├── main.py            # FastAPI entry point
├── requirements.txt   # Python dependencies
└── README.md          # This file
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

## ▶️ Running the Game

### 1. Start the Backend Server
```bash
python main.py
```
The backend will start on `http://127.0.0.1:8002`

### 2. Start the Frontend Server
```bash
cd web
python -m http.server 8080
```

### 3. Play the Game
Open your browser and navigate to `http://localhost:8080`

## 🎮 How to Play

- **W** - Move Up (Forward)
- **S** - Move Down (Backward)
- **A** - Move Left
- **D** - Move Right

Objective: Survive for 15 seconds without hitting the wind obstacles.

## 🤖 Reinforcement Learning Model

This game uses a Deep Q-Network (DQN) trained with Stable Baselines3. The model was trained in the custom airplane environment defined in `env/env.py`.

### Training Process
The model learns to:
1. Observe the plane's position
2. Track wind obstacle locations
3. Make decisions to move left, right, or stay in place
4. Maximize survival time

### Environment Details
- **Actions**: 3 discrete actions (Left, Stay, Right)
- **Observations**: Plane X, Plane Y, Wind X, Time Remaining
- **Reward**: +1 for each timestep survived, -10 for collision

## 📂 Directory Explanation

- **env/**: Contains the custom Gymnasium environment where the RL agent learns
- **models/**: Stores the trained DQN model weights
- **src/**: FastAPI backend that serves predictions to the frontend
- **training/**: Scripts to train new models
- **web/**: Frontend game interface (HTML/CSS/JS)

## 🧪 Training a New Model

To train a new model:
```bash
cd training
python train.py
```

This will save the trained model to `models/plane_dqn_model.zip`.