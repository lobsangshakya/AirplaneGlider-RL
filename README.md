Airplane Glider – RL Game

A simple reinforcement-learning project where a DQN agent learns to glide an airplane while avoiding wind obstacles. Includes a custom Gym environment, training script, FastAPI backend, and a minimal browser game UI.

Environment

Observations: plane_x, plane_y, wind_x, time_remaining

Actions: 0 = left, 1 = stay, 2 = right

Rewards: +1 survive, -10 crash, +5 full survival

Installation
git clone https://github.com/lobsangshakya/AirplaneGlider-RL.git
cd AirplaneGlider-RL
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Training
python train.py

Run Backend
uvicorn app:app --reload


Endpoint:
POST http://127.0.0.1:8000/predict_action

Frontend

Open frontend/index.html to play the game (plane controlled automatically by the model).

System Requirements

Python 3.8+

macOS/Windows/Linux

Any modern browser
