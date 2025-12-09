#!/usr/bin/env python3
"""
2D Airplane Landing Simulator
A simple physics-based simulator where players control left/right engine thrust to balance the airplane during descent.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Create FastAPI app
app = FastAPI(title="2D Airplane Landing Simulator", description="Control airplane thrust for balanced landing")

# HTML template with embedded CSS and JS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2D Airplane Landing Simulator</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #87CEEB, #B0E2FF);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #333;
        }

        .container {
            text-align: center;
            max-width: 800px;
            width: 100%;
        }

        h1 {
            font-size: 2rem;
            margin: 0 0 15px 0;
            color: #01579B;
        }

        .instructions {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .game-area {
            width: 600px;
            height: 400px;
            margin: 0 auto;
            position: relative;
            background: linear-gradient(to bottom, #E0F7FF, #B0E2FF);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 2px solid #87CEEB;
        }

        #airplane {
            position: absolute;
            width: 80px;
            height: 30px;
            transition: transform 0.1s ease;
        }

        #left-engine-flame {
            position: absolute;
            width: 25px;
            height: 12px;
            background: linear-gradient(to right, orange, red, yellow);
            border-radius: 50% 0 0 50%;
            opacity: 0;
            transition: opacity 0.1s;
            box-shadow: 0 0 10px orange;
        }

        #right-engine-flame {
            position: absolute;
            width: 25px;
            height: 12px;
            background: linear-gradient(to left, orange, red, yellow);
            border-radius: 0 50% 50% 0;
            opacity: 0;
            transition: opacity 0.1s;
            box-shadow: 0 0 10px orange;
        }

        .ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 40px;
            background: linear-gradient(to top, #8B4513, #A0522D);
        }

        .runway {
            position: absolute;
            bottom: 40px;
            width: 100%;
            height: 20px;
            background: linear-gradient(to right, #555, #777, #555);
        }

        .controls {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
        }

        .key {
            width: 80px;
            height: 80px;
            background: #0288D1;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .key.active {
            background: #0277BD;
            transform: translateY(2px);
        }

        .status {
            margin-top: 20px;
            font-size: 1.2rem;
            font-weight: bold;
            color: #01579B;
        }

        .altitude-bar {
            position: absolute;
            right: 20px;
            top: 20px;
            width: 30px;
            height: 300px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            overflow: hidden;
        }

        .altitude-fill {
            position: absolute;
            bottom: 0;
            width: 100%;
            background: #4CAF50;
            transition: height 0.3s;
        }

        .crash-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 0, 0, 0.7);
            display: none;
            justify-content: center;
            align-items: center;
            font-size: 3rem;
            color: white;
            font-weight: bold;
            z-index: 100;
        }

        .success-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 255, 0, 0.7);
            display: none;
            justify-content: center;
            align-items: center;
            font-size: 3rem;
            color: white;
            font-weight: bold;
            z-index: 100;
        }

        @media (max-width: 650px) {
            .game-area {
                width: 95%;
                height: 300px;
            }
            
            .controls {
                gap: 15px;
            }
            
            .key {
                width: 60px;
                height: 60px;
                font-size: 1.2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✈️ 2D Airplane Landing Simulator</h1>
        
        <div class="instructions">
            <p>Use LEFT and RIGHT arrow keys to control engine thrust</p>
            <p>Left Engine: Tilt plane RIGHT | Right Engine: Tilt plane LEFT</p>
        </div>
        
        <div class="game-area" id="gameArea">
            <svg id="airplane" width="80" height="30" viewBox="0 0 80 30">
                <polygon points="0,15 60,5 60,25" fill="#1976D2"/>
                <polygon points="60,5 75,15 60,25" fill="#0D47A1"/>
                <circle cx="20" cy="15" r="5" fill="#E0E0E0"/>
            </svg>
            
            <div id="left-engine-flame"></div>
            <div id="right-engine-flame"></div>
            
            <div class="runway"></div>
            <div class="ground"></div>
            
            <div class="altitude-bar">
                <div class="altitude-fill" id="altitudeFill"></div>
            </div>
            
            <div class="crash-animation" id="crashAnimation">💥 CRASH!</div>
            <div class="success-animation" id="successAnimation">✅ SUCCESS!</div>
        </div>
        
        <div class="controls">
            <div class="key" id="leftKey">←</div>
            <div class="key" id="rightKey">→</div>
        </div>
        
        <div class="status" id="status">Altitude: 300ft | Speed: 20 mph | Angle: 0°</div>
    </div>
    
    <script>
        // Game variables
        let airplaneX = 300;
        let airplaneY = 50;
        let airplaneAngle = 0;
        let velocityX = 0;
        let velocityY = 0.5; // Slower descent speed
        let angularVelocity = 0;
        let altitude = 300;
        let speed = 20;
        let gameRunning = true;
        
        // DOM elements
        const airplane = document.getElementById('airplane');
        const leftFlame = document.getElementById('left-engine-flame');
        const rightFlame = document.getElementById('right-engine-flame');
        const leftKey = document.getElementById('leftKey');
        const rightKey = document.getElementById('rightKey');
        const status = document.getElementById('status');
        const altitudeFill = document.getElementById('altitudeFill');
        const gameArea = document.getElementById('gameArea');
        const crashAnimation = document.getElementById('crashAnimation');
        const successAnimation = document.getElementById('successAnimation');
        
        // Initialize positions
        updateAirplanePosition();
        
        // Keyboard event listeners
        document.addEventListener('keydown', function(event) {
            if (!gameRunning) return;
            
            switch(event.key) {
                case 'ArrowLeft':
                    activateLeftEngine();
                    event.preventDefault();
                    break;
                case 'ArrowRight':
                    activateRightEngine();
                    event.preventDefault();
                    break;
            }
        });
        
        document.addEventListener('keyup', function(event) {
            switch(event.key) {
                case 'ArrowLeft':
                    deactivateLeftEngine();
                    event.preventDefault();
                    break;
                case 'ArrowRight':
                    deactivateRightEngine();
                    event.preventDefault();
                    break;
            }
        });
        
        // Touch events for mobile
        leftKey.addEventListener('touchstart', function(e) {
            e.preventDefault();
            activateLeftEngine();
        });
        
        leftKey.addEventListener('touchend', function(e) {
            e.preventDefault();
            deactivateLeftEngine();
        });
        
        rightKey.addEventListener('touchstart', function(e) {
            e.preventDefault();
            activateRightEngine();
        });
        
        rightKey.addEventListener('touchend', function(e) {
            e.preventDefault();
            deactivateRightEngine();
        });
        
        // Mouse events for desktop
        leftKey.addEventListener('mousedown', activateLeftEngine);
        leftKey.addEventListener('mouseup', deactivateLeftEngine);
        leftKey.addEventListener('mouseleave', deactivateLeftEngine);
        
        rightKey.addEventListener('mousedown', activateRightEngine);
        rightKey.addEventListener('mouseup', deactivateRightEngine);
        rightKey.addEventListener('mouseleave', deactivateRightEngine);
        
        function activateLeftEngine() {
            leftKey.classList.add('active');
            leftFlame.style.opacity = '1';
            
            // Apply left thrust (creates counter-clockwise rotation - tilts plane RIGHT)
            velocityX -= 0.2;
            angularVelocity -= 0.8; // Negative for counter-clockwise rotation
        }
        
        function deactivateLeftEngine() {
            leftKey.classList.remove('active');
            leftFlame.style.opacity = '0';
        }
        
        function activateRightEngine() {
            rightKey.classList.add('active');
            rightFlame.style.opacity = '1';
            
            // Apply right thrust (creates clockwise rotation - tilts plane LEFT)
            velocityX += 0.2;
            angularVelocity += 0.8; // Positive for clockwise rotation
        }
        
        function deactivateRightEngine() {
            rightKey.classList.remove('active');
            rightFlame.style.opacity = '0';
        }
        
        function updateAirplanePosition() {
            airplane.style.left = (airplaneX - 40) + 'px';
            airplane.style.top = airplaneY + 'px';
            airplane.style.transform = `rotate(${airplaneAngle}deg)`;
            
            leftFlame.style.left = (airplaneX - 55) + 'px';
            leftFlame.style.top = (airplaneY + 9) + 'px';
            
            rightFlame.style.left = (airplaneX + 30) + 'px';
            rightFlame.style.top = (airplaneY + 9) + 'px';
        }
        
        function updateStatus() {
            status.textContent = `Altitude: ${Math.round(altitude)}ft | Speed: ${Math.round(speed)} mph | Angle: ${Math.round(airplaneAngle)}°`;
            altitudeFill.style.height = (altitude / 300 * 100) + '%';
        }
        
        function showCrash() {
            crashAnimation.style.display = 'flex';
            gameRunning = false;
        }
        
        function showSuccess() {
            successAnimation.style.display = 'flex';
            gameRunning = false;
        }
        
        // Game loop
        function gameLoop() {
            if (!gameRunning) return;
            
            // Apply reduced gravity for slower descent
            velocityY += 0.05;
            
            // Apply angular damping (natural stabilization)
            angularVelocity *= 0.95;
            airplaneAngle += angularVelocity;
            
            // Apply air resistance
            velocityX *= 0.98;
            velocityY *= 0.995;
            
            // Update position
            airplaneX += velocityX;
            airplaneY += velocityY;
            
            // Update altitude and speed
            altitude = 300 - airplaneY;
            speed = Math.sqrt(velocityX * velocityX + velocityY * velocityY) * 10;
            
            // Boundary checks
            if (airplaneX < 40) airplaneX = 40;
            if (airplaneX > 560) airplaneX = 560;
            
            // Ground collision
            if (airplaneY > 320) {
                airplaneY = 320;
                velocityY = 0;
                
                // Check landing success
                if (Math.abs(airplaneAngle) < 10 && Math.abs(velocityX) < 2) {
                    showSuccess();
                } else {
                    showCrash();
                }
            }
            
            // Update airplane position and status
            updateAirplanePosition();
            updateStatus();
            
            // Continue game loop
            requestAnimationFrame(gameLoop);
        }
        
        // Start the game
        gameLoop();
    </script>
</body>
</html>
"""

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main game page"""
    return HTML_TEMPLATE

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting 2D Airplane Landing Simulator...")
    print("🎮 Access the game at: http://localhost:8004")
    uvicorn.run(app, host="127.0.0.1", port=8004)