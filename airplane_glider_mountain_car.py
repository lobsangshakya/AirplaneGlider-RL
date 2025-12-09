#!/usr/bin/env python3
"""
Airplane Glider Game - Mountain Car Style Implementation
A reinforcement learning-powered airplane glider game with physics-based movement similar to Mountain Car.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import numpy as np
from stable_baselines3 import DQN
from pydantic import BaseModel

# Pydantic model for game state
class GameState(BaseModel):
    plane_x: float
    plane_y: float
    velocity_x: float
    velocity_y: float
    wind_x: float
    time_remaining: float

# Create FastAPI app
app = FastAPI(title="Mountain Car Airplane Glider", description="Physics-based airplane glider game")

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
    model_path = "models/mountain_car_plane_dqn_model.zip"
    if os.path.exists(model_path):
        model = DQN.load(model_path)
        print("Mountain Car model loaded successfully!")
    else:
        print("Mountain Car model file not found. AI control will not be available.")
        # Try fallback to original model
        fallback_path = "models/plane_dqn_model.zip"
        if os.path.exists(fallback_path):
            model = DQN.load(fallback_path)
            print("Fallback to original model successful!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# HTML template with Mountain Car-style visualization
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mountain Car Airplane Glider</title>
    <style>
        /* Global Styles */
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #1a237e, #4a148c);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
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
            color: #bb86fc;
            text-shadow: 0 0 10px rgba(187, 134, 252, 0.5);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 400px;
            margin: 0 auto 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .stat-item {
            font-size: 0.9rem;
        }

        .stat-value {
            font-weight: bold;
            font-size: 1.1rem;
            color: #bb86fc;
        }

        /* Game Area Styles */
        #gameArea {
            width: 400px;
            height: 600px;
            margin: 0 auto;
            position: relative;
            background: linear-gradient(to bottom, #0d47a1, #1a237e);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            border: 3px solid #5e35b1;
        }

        /* Airplane Styles */
        #plane {
            position: absolute;
            width: 40px;
            height: 20px;
            z-index: 10;
            transition: transform 0.1s ease;
        }

        /* Velocity vector indicator */
        #velocityVector {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #00ff00;
            border-radius: 50%;
            z-index: 9;
            box-shadow: 0 0 10px #00ff00;
        }

        /* Wind/Obstacle Styles */
        #wind {
            position: absolute;
            width: 30px;
            height: 30px;
            z-index: 5;
        }

        /* Ground and sky visualization */
        #ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 30px;
            background: linear-gradient(to top, #388e3c, #4caf50);
            z-index: 1;
        }

        /* Controls Styles */
        .controls {
            margin-top: 25px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        .controls h2 {
            margin-top: 0;
            color: #bb86fc;
        }

        .control-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 15px 0;
        }

        .control-btn {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(145deg, #6200ea, #3700b3);
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: all 0.2s ease;
        }

        .control-btn:active {
            transform: scale(0.95);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        .control-btn.left { background: linear-gradient(145deg, #03dac6, #018786); }
        .control-btn.right { background: linear-gradient(145deg, #03dac6, #018786); }
        .control-btn.up { background: linear-gradient(145deg, #bb86fc, #3700b3); }

        button#startButton {
            margin-top: 15px;
            padding: 15px 40px;
            font-size: 1.2rem;
            background: linear-gradient(145deg, #03dac6, #018786);
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            font-weight: bold;
        }

        button#startButton:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }

        button#startButton:active {
            transform: translateY(1px);
        }

        button#startButton:disabled {
            background: linear-gradient(145deg, #9e9e9e, #616161);
            cursor: not-allowed;
            transform: none;
        }

        /* Info panel */
        .info-panel {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            font-size: 0.9rem;
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
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⛰️ Mountain Car Airplane Glider</h1>
            <div class="stats">
                <div class="stat-item">
                    <div>Altitude</div>
                    <div class="stat-value" id="altitude">550.0</div>
                </div>
                <div class="stat-item">
                    <div>Velocity</div>
                    <div class="stat-value" id="velocity">0.0</div>
                </div>
                <div class="stat-item">
                    <div>Time</div>
                    <div class="stat-value" id="time">15.0</div>
                </div>
            </div>
        </header>
        
        <div id="gameArea">
            <!-- Airplane SVG -->
            <svg id="plane" width="40" height="20" viewBox="0 0 40 20">
                <polygon points="0,10 30,5 30,15" fill="#03dac6"/>
                <polygon points="5,10 20,7 20,13" fill="#018786"/>
                <polygon points="25,10 35,8 35,12" fill="#018786"/>
            </svg>
            
            <!-- Velocity vector -->
            <div id="velocityVector"></div>
            
            <!-- Wind obstacle SVG -->
            <svg id="wind" width="30" height="30" viewBox="0 0 30 30">
                <circle cx="15" cy="15" r="12" fill="rgba(255,69,0,0.7)"/>
                <path d="M8,12 Q15,10 22,12" stroke="white" stroke-width="2" fill="none"/>
                <path d="M8,18 Q15,16 22,18" stroke="white" stroke-width="2" fill="none"/>
            </svg>
            
            <!-- Ground -->
            <div id="ground"></div>
        </div>
        
        <div class="controls">
            <h2>Controls</h2>
            <div class="control-buttons">
                <button class="control-btn left" id="leftBtn">←</button>
                <button class="control-btn up" id="upBtn">↑</button>
                <button class="control-btn right" id="rightBtn">→</button>
            </div>
            <button id="startButton" type="button">Start Game</button>
        </div>
        
        <div class="info-panel">
            <p>Physics-based flight simulation with velocity and momentum</p>
            <p>Use arrow buttons or keyboard: ← ↑ →</p>
        </div>
    </div>
    
    <script>
        // Get DOM elements
        const plane = document.getElementById("plane");
        const wind = document.getElementById("wind");
        const velocityVector = document.getElementById("velocityVector");
        const startButton = document.getElementById("startButton");
        const leftBtn = document.getElementById("leftBtn");
        const rightBtn = document.getElementById("rightBtn");
        const upBtn = document.getElementById("upBtn");
        
        // Stat displays
        const altitudeDisplay = document.getElementById("altitude");
        const velocityDisplay = document.getElementById("velocity");
        const timeDisplay = document.getElementById("time");

        // Game variables
        let planeX = 200;
        let planeY = 550;
        let velocityX = 0;
        let velocityY = 0;
        let windX = 150;
        let windY = 0;
        let timeRemaining = 15;
        let interval;
        let gameActive = false;

        // Initialize positions
        plane.style.left = planeX + "px";
        plane.style.bottom = planeY + "px";
        wind.style.left = windX + "px";
        wind.style.top = windY + "px";
        velocityVector.style.left = planeX + 20 + "px";
        velocityVector.style.bottom = planeY + 10 + "px";

        // Update displays
        altitudeDisplay.textContent = planeY.toFixed(1);
        velocityDisplay.textContent = Math.sqrt(velocityX*velocityX + velocityY*velocityY).toFixed(2);
        timeDisplay.textContent = timeRemaining.toFixed(1);

        // Control event handlers
        function moveLeft() {
            if (!gameActive) return;
            velocityX -= 0.03; // Apply left thrust
        }

        function moveRight() {
            if (!gameActive) return;
            velocityX += 0.03; // Apply right thrust
        }

        function moveUp() {
            if (!gameActive) return;
            velocityY += 0.05; // Apply upward thrust
        }

        // Button event listeners
        leftBtn.addEventListener("click", moveLeft);
        rightBtn.addEventListener("click", moveRight);
        upBtn.addEventListener("click", moveUp);

        // Keyboard event listeners
        document.addEventListener("keydown", function(event) {
            if (!gameActive) return;
            
            switch(event.key) {
                case "ArrowLeft":
                    moveLeft();
                    event.preventDefault();
                    break;
                case "ArrowRight":
                    moveRight();
                    event.preventDefault();
                    break;
                case "ArrowUp":
                    moveUp();
                    event.preventDefault();
                    break;
            }
        });

        // Start game function
        function startGame() {
            // Reset game state
            planeX = 200;
            planeY = 550;
            velocityX = 0;
            velocityY = 0;
            windX = Math.floor(Math.random() * 350);
            windY = 0;
            timeRemaining = 15;
            gameActive = true;
            
            // Update displays
            altitudeDisplay.textContent = planeY.toFixed(1);
            velocityDisplay.textContent = Math.sqrt(velocityX*velocityX + velocityY*velocityY).toFixed(2);
            timeDisplay.textContent = timeRemaining.toFixed(1);
            
            // Update positions
            plane.style.left = planeX + "px";
            plane.style.bottom = planeY + "px";
            wind.style.left = windX + "px";
            wind.style.top = windY + "px";
            velocityVector.style.left = planeX + 20 + "px";
            velocityVector.style.bottom = planeY + 10 + "px";
            
            // Disable button during gameplay
            startButton.disabled = true;
            startButton.textContent = "Playing...";
            
            // Start game loop
            interval = setInterval(() => {
                // Apply physics
                velocityY -= 0.05; // Gravity
                
                // Update positions based on velocities
                planeX += velocityX * 10;
                planeY += velocityY * 10;
                
                // Boundary checks
                if (planeX < 0) {
                    planeX = 0;
                    velocityX = 0;
                }
                if (planeX > 360) {
                    planeX = 360;
                    velocityX = 0;
                }
                if (planeY < 30) { // Ground level
                    planeY = 30;
                    velocityY = 0;
                }
                if (planeY > 580) {
                    planeY = 580;
                    velocityY = 0;
                }
                
                // Update plane position
                plane.style.left = planeX + "px";
                plane.style.bottom = planeY + "px";
                
                // Update velocity vector indicator
                velocityVector.style.left = (planeX + 20 + velocityX * 50) + "px";
                velocityVector.style.bottom = (planeY + 10 + velocityY * 50) + "px";
                
                // Move wind down
                windY += 2;
                wind.style.top = windY + "px";
                
                // Collision check
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
                    alert("💥 CRASHED! Game Over.");
                    clearInterval(interval);
                    gameActive = false;
                    startButton.disabled = false;
                    startButton.textContent = "Play Again";
                    return;
                }
                
                // Timer
                timeRemaining -= 0.1;
                
                // Update displays
                altitudeDisplay.textContent = planeY.toFixed(1);
                velocityDisplay.textContent = Math.sqrt(velocityX*velocityX + velocityY*velocityY).toFixed(2);
                timeDisplay.textContent = timeRemaining.toFixed(1);
                
                // Game over when time runs out
                if (timeRemaining <= 0) {
                    alert("🎉 Success! You survived! Final Altitude: " + planeY.toFixed(1));
                    clearInterval(interval);
                    gameActive = false;
                    startButton.disabled = false;
                    startButton.textContent = "Play Again";
                    return;
                }
                
                // Reset wind when it goes off screen
                if (windY > 600) {
                    windY = -30;
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
        # For Mountain Car-style environment, we have 6 observations
        obs = np.array([
            state.plane_x,
            state.plane_y,
            state.velocity_x,
            state.velocity_y,
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
    return {"status": "healthy", "model_loaded": model is not None, "model_type": "mountain_car"}

if __name__ == "__main__":
    print("🚀 Starting Mountain Car Airplane Glider Game...")
    print("🎮 Access the game at: http://localhost:8003")
    print("ℹ️  Use port 8003 to avoid conflicts with other servers")
    uvicorn.run(app, host="127.0.0.1", port=8003)
