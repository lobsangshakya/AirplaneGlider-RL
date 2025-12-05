#!/usr/bin/env python3
"""
Airplane Glider Game - Python Implementation
A reinforcement learning-powered airplane glider game where players control an airplane to avoid wind obstacles.
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from stable_baselines3 import DQN
from pydantic import BaseModel

# Game constants
GAME_WIDTH = 400
GAME_HEIGHT = 600
PLANE_WIDTH = 40
PLANE_HEIGHT = 20
WIND_WIDTH = 30
WIND_HEIGHT = 30

# Pydantic model for game state
class GameState(BaseModel):
    plane_x: float
    plane_y: float
    wind_x: float
    time_remaining: float

# Create FastAPI app
app = FastAPI(title="Airplane Glider Game", description="A reinforcement learning-powered airplane glider game")

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model = None
try:
    if os.path.exists("models/plane_dqn_model.zip"):
        model = DQN.load("models/plane_dqn_model.zip")
        print("Model loaded successfully!")
    else:
        print("Model file not found. AI control will not be available.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airplane Glider RL</title>
    <style>
        /* Global Styles */
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #87CEEB, #B0E2FF);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }

        .container {
            text-align: center;
            max-width: 500px;
            width: 100%;
        }

        /* Header Styles */
        header {
            margin-bottom: 20px;
        }

        h1 {
            font-size: 2rem;
            margin: 0 0 15px 0;
            color: #01579B;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            max-width: 400px;
            margin: 0 auto;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .timer, .score {
            font-size: 1.1rem;
            font-weight: bold;
        }

        /* Game Area Styles */
        #gameArea {
            width: 400px;
            height: 600px;
            margin: 0 auto;
            position: relative;
            background: linear-gradient(to bottom, #E0F7FF, #B0E2FF);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 2px solid #87CEEB;
        }

        /* Airplane Styles */
        #plane {
            position: absolute;
            bottom: 50px;
            left: 180px;
            z-index: 10;
            transition: transform 0.1s ease;
        }

        /* Wind/Obstacle Styles */
        #wind {
            position: absolute;
            top: -30px;
            left: 150px;
            z-index: 5;
        }

        /* Controls Styles */
        .controls {
            margin-top: 20px;
        }

        .controls p {
            margin: 10px 0;
            color: #01579B;
            font-weight: bold;
        }

        button {
            margin-top: 10px;
            padding: 12px 30px;
            font-size: 1.1rem;
            background: #0288D1;
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            font-weight: bold;
        }

        button:hover {
            background: #0277BD;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }

        button:active {
            transform: translateY(1px);
        }

        button:disabled {
            background: #90A4AE;
            cursor: not-allowed;
            transform: none;
        }

        /* Responsive Design */
        @media (max-width: 500px) {
            #gameArea {
                width: 350px;
                height: 525px;
            }
            
            h1 {
                font-size: 1.8rem;
            }
            
            .stats {
                padding: 8px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Airplane Glider</h1>
            <div class="stats">
                <div class="timer">Time: <span id="time">15.0</span>s</div>
                <div class="score">Score: <span id="score">0</span></div>
            </div>
        </header>
        
        <div id="gameArea">
            <!-- Airplane SVG -->
            <svg id="plane" width="40" height="20" viewBox="0 0 40 20">
                <polygon points="0,10 30,5 30,15" fill="#1976D2"/>
                <polygon points="5,10 20,7 20,13" fill="#0D47A1"/>
                <polygon points="25,10 35,8 35,12" fill="#0D47A1"/>
            </svg>
            
            <!-- Wind obstacle SVG -->
            <svg id="wind" width="30" height="30" viewBox="0 0 30 30">
                <circle cx="15" cy="15" r="12" fill="rgba(128,128,128,0.7)"/>
                <path d="M8,12 Q15,10 22,12" stroke="white" stroke-width="2" fill="none"/>
                <path d="M8,18 Q15,16 22,18" stroke="white" stroke-width="2" fill="none"/>
            </svg>
        </div>
        
        <div class="controls">
            <p>Controls: W (Up) · S (Down) · A (Left) · D (Right)</p>
            <button id="startButton" type="button">Start Game</button>
        </div>
    </div>
    
    <script>
        // Get DOM elements
        const plane = document.getElementById("plane");
        const wind = document.getElementById("wind");
        const startButton = document.getElementById("startButton");
        const timeDisplay = document.getElementById("time");
        const scoreDisplay = document.getElementById("score");

        // Game variables
        let planeX = 180;
        let planeY = 550;
        let windX = 150;
        let windY = -40;  // Start wind off-screen
        let timeRemaining = 15;
        let score = 0;
        let interval;
        let gameActive = false;

        // Movement variables
        let moveLeft = false;
        let moveRight = false;
        let moveForward = false;
        let moveBackward = false;

        // Initialize positions
        plane.style.left = planeX + "px";
        plane.style.bottom = planeY + "px";
        wind.style.left = windX + "px";
        wind.style.top = windY + "px";

        // Update displays
        timeDisplay.textContent = timeRemaining.toFixed(1);
        scoreDisplay.textContent = score;

        // Keyboard event listeners
        document.addEventListener("keydown", function(event) {
            if (!gameActive) return;
            
            switch(event.key.toLowerCase()) {
                case "a":
                    moveLeft = true;
                    event.preventDefault();
                    break;
                case "d":
                    moveRight = true;
                    event.preventDefault();
                    break;
                case "w":
                    moveForward = true;
                    event.preventDefault();
                    break;
                case "s":
                    moveBackward = true;
                    event.preventDefault();
                    break;
            }
        });

        document.addEventListener("keyup", function(event) {
            if (!gameActive) return;
            
            switch(event.key.toLowerCase()) {
                case "a":
                    moveLeft = false;
                    break;
                case "d":
                    moveRight = false;
                    break;
                case "w":
                    moveForward = false;
                    break;
                case "s":
                    moveBackward = false;
                    break;
            }
        });

        // Start game function
        function startGame() {
            // Reset game state
            planeX = 180;
            planeY = 550;
            windX = Math.floor(Math.random() * 350);  // Random starting position
            windY = -40;  // Start wind off-screen
            timeRemaining = 15;
            score = 0;
            gameActive = true;
            
            // Reset movement
            moveLeft = false;
            moveRight = false;
            moveForward = false;
            moveBackward = false;
            
            // Update displays
            timeDisplay.textContent = timeRemaining.toFixed(1);
            scoreDisplay.textContent = score;
            
            // Update positions
            plane.style.left = planeX + "px";
            plane.style.bottom = planeY + "px";
            wind.style.left = windX + "px";
            wind.style.top = windY + "px";
            
            // Disable button during gameplay
            startButton.disabled = true;
            startButton.textContent = "Playing...";
            
            // Start game loop
            interval = setInterval(() => {
                // Player controls
                if (moveLeft) planeX -= 8;
                if (moveRight) planeX += 8;
                if (moveForward) planeY += 5;  // Move up
                if (moveBackward) planeY -= 3; // Move down (slower than natural glide)
                
                // Boundary checks
                if (planeX < 0) planeX = 0;
                if (planeX > 360) planeX = 360;
                if (planeY < 0) planeY = 0;
                if (planeY > 560) planeY = 560;
                
                // Update plane position
                plane.style.left = planeX + "px";
                plane.style.bottom = planeY + "px";
                
                // Natural glide (plane moves down over time)
                planeY -= 5;
                plane.style.bottom = planeY + "px";
                
                // Move wind down
                windY += 5;
                wind.style.top = windY + "px";
                
                // Manual collision detection (using bounding boxes)
                const planeLeft = planeX;
                const planeRight = planeX + 40;
                const planeTop = 600 - planeY - 20;
                const planeBottom = 600 - planeY;
                
                const windLeft = windX;
                const windRight = windX + 30;
                const windTop = windY;
                const windBottom = windY + 30;
                
                // Check for collision
                if (planeLeft < windRight && 
                    planeRight > windLeft && 
                    planeTop < windBottom && 
                    planeBottom > windTop) {
                    alert("CRASHED! Game Over.");
                    clearInterval(interval);
                    gameActive = false;
                    startButton.disabled = false;
                    startButton.textContent = "Play Again";
                    return;
                }
                
                // Timer and scoring
                timeRemaining -= 0.1;
                score += 1; // Increase score over time
                
                // Update displays
                timeDisplay.textContent = timeRemaining.toFixed(1);
                scoreDisplay.textContent = score;
                
                // Game over when time runs out
                if (timeRemaining <= 0) {
                    alert("Success! You survived! Final Score: " + score);
                    clearInterval(interval);
                    gameActive = false;
                    startButton.disabled = false;
                    startButton.textContent = "Play Again";
                    return;
                }
                
                // Reset wind when it goes off screen
                if (windY > 640) {
                    windY = -40;
                    wind.style.top = windY + "px";
                    windX = Math.floor(Math.random() * 350);
                    wind.style.left = windX + "px";
                }
            }, 100);
        }

        // Add event listener to button
        startButton.addEventListener("click", startGame);
    </script>
</body>
</html>
"""

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main game page"""
    return HTML_TEMPLATE

@app.post("/predict_action")
async def predict_action(state: GameState):
    """Predict action using the trained RL model"""
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        obs = np.array([
            state.plane_x,
            state.plane_y,
            state.wind_x,
            state.time_remaining
        ], dtype=np.float32)
        
        # Stable Baselines correct function is `.predict()`
        action, _ = model.predict(obs)
        return {"action": int(action)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    print("Starting Airplane Glider Game...")
    print("Access the game at: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)