from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from stable_baselines3 import DQN

app = FastAPI()

# --- ENABLE CORS so frontend can call backend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load AI Model ---
try:
    model = DQN.load("models/plane_dqn_model.zip")
    print("Model loaded successfully!")
except Exception as e:
    print("ERROR loading model:", e)
    model = None


# --- Incoming data format ---
class GameState(BaseModel):
    plane_x: float
    plane_y: float
    wind_x: float
    time_remaining: float


# --- Test Route ---
@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}


# --- Prediction Route used by your game ---
@app.post("/predict_action")
def predict_action(state: GameState):

    if model is None:
        return {"error": "Model not loaded"}

    obs = np.array([
        state.plane_x,
        state.plane_y,
        state.wind_x,
        state.time_remaining
    ], dtype=np.float32)

    # Stable Baselines correct function is `.predict()`
    action, _ = model.predict(obs)

    return {"action": int(action)}