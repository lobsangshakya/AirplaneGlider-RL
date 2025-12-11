#!/usr/bin/env python3
"""
Realistic 2D Rocket Landing Simulator
A clean implementation with realistic physics for rocket landing simulation.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Create FastAPI app
app = FastAPI(title="Realistic Rocket Landing Simulator", description="2D rocket landing with realistic physics")

# HTML template with embedded CSS and JS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Realistic Rocket Landing Simulator</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #0c1445, #1a237e);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #e0e0e0;
        }

        .container {
            text-align: center;
            max-width: 800px;
            width: 100%;
        }

        h1 {
            font-size: 2rem;
            margin: 0 0 15px 0;
            color: #bb86fc;
            text-shadow: 0 0 10px rgba(187, 134, 252, 0.5);
        }

        .instructions {
            background: rgba(30, 30, 46, 0.8);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .game-area {
            width: 600px;
            height: 400px;
            margin: 0 auto;
            position: relative;
            background: linear-gradient(to bottom, #151d3b, #0f162d);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            border: 2px solid #5e35b1;
        }

        #rocket {
            position: absolute;
            width: 40px;
            height: 40px;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        #left-engine-flame {
            position: absolute;
            width: 20px;
            height: 30px;
            background: linear-gradient(to top, #ff5722, #ff9800, #ffff00);
            border-radius: 50% 50% 0 0;
            opacity: 0;
            transition: opacity 0.15s ease, height 0.2s ease;
            box-shadow: 0 0 15px #ff5722;
        }

        #right-engine-flame {
            position: absolute;
            width: 20px;
            height: 30px;
            background: linear-gradient(to top, #ff5722, #ff9800, #ffff00);
            border-radius: 50% 50% 0 0;
            opacity: 0;
            transition: opacity 0.15s ease, height 0.2s ease;
            box-shadow: 0 0 15px #ff5722;
        }

        .center-engine-flame {
            position: absolute;
            width: 25px;
            height: 40px;
            background: linear-gradient(to top, #ff5722, #ff9800, #ffff00);
            border-radius: 50% 50% 0 0;
            opacity: 0.7;
            transition: height 0.3s ease;
            box-shadow: 0 0 20px #ff5722;
        }

        .ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 40px;
            background: linear-gradient(to top, #3e2723, #4e342e);
        }

        .landing-pad {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 120px;
            height: 15px;
            background: linear-gradient(to right, #7b1fa2, #9c27b0, #7b1fa2);
            border-radius: 5px 5px 0 0;
            box-shadow: 0 0 20px rgba(156, 39, 176, 0.5);
        }

        .landing-lights {
            position: absolute;
            bottom: 42px;
            left: 50%;
            transform: translateX(-50%);
            width: 130px;
            display: flex;
            justify-content: space-around;
        }

        .landing-light {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #ff5252;
            box-shadow: 0 0 10px #ff5252;
            animation: pulse 1.5s infinite;
        }

        .controls {
            margin-top: 25px;
            display: flex;
            justify-content: center;
            gap: 40px;
        }

        .key {
            width: 90px;
            height: 90px;
            background: linear-gradient(145deg, #6200ea, #3700b3);
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 1.8rem;
            font-weight: bold;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            transition: all 0.2s ease;
        }

        .key.active {
            transform: translateY(4px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            background: linear-gradient(145deg, #3700b3, #6200ea);
        }

        .status {
            margin-top: 25px;
            font-size: 1.3rem;
            font-weight: bold;
            color: #bb86fc;
            text-shadow: 0 0 8px rgba(187, 134, 252, 0.5);
            background: rgba(30, 30, 46, 0.6);
            padding: 15px 30px;
            border-radius: 30px;
            backdrop-filter: blur(5px);
        }

        .altitude-bar {
            position: absolute;
            right: 20px;
            top: 20px;
            width: 30px;
            height: 300px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .altitude-fill {
            position: absolute;
            bottom: 0;
            width: 100%;
            background: linear-gradient(to top, #4caf50, #8bc34a);
            transition: height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .crash-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 0, 0, 0.85);
            display: none;
            justify-content: center;
            align-items: center;
            font-size: 3.5rem;
            color: white;
            font-weight: bold;
            z-index: 100;
            animation: shake 0.6s infinite;
        }

        .success-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 128, 0, 0.85);
            display: none;
            justify-content: center;
            align-items: center;
            font-size: 3.5rem;
            color: white;
            font-weight: bold;
            z-index: 100;
            animation: success-pulse 2s infinite;
        }

        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-2px, -3px) rotate(-2deg); }
            20% { transform: translate(-4px, 0px) rotate(2deg); }
            30% { transform: translate(4px, 3px) rotate(0deg); }
            40% { transform: translate(2px, -2px) rotate(2deg); }
            50% { transform: translate(-2px, 3px) rotate(-2deg); }
            60% { transform: translate(-4px, 1px) rotate(0deg); }
            70% { transform: translate(4px, 1px) rotate(-2deg); }
            80% { transform: translate(-2px, -2px) rotate(2deg); }
            90% { transform: translate(2px, 3px) rotate(0deg); }
            100% { transform: translate(1px, -3px) rotate(-1deg); }
        }

        @keyframes pulse {
            0% { opacity: 0.4; box-shadow: 0 0 5px #ff5252; }
            50% { opacity: 1; box-shadow: 0 0 20px #ff5252; }
            100% { opacity: 0.4; box-shadow: 0 0 5px #ff5252; }
        }

        @keyframes success-pulse {
            0% { background: rgba(0, 128, 0, 0.85); }
            50% { background: rgba(0, 200, 0, 0.9); }
            100% { background: rgba(0, 128, 0, 0.85); }
        }

        @media (max-width: 650px) {
            .game-area {
                width: 95%;
                height: 300px;
            }
            
            .controls {
                gap: 20px;
            }
            
            .key {
                width: 70px;
                height: 70px;
                font-size: 1.5rem;
            }
            
            h1 {
                font-size: 1.7rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Realistic Rocket Landing Simulator</h1>
        
        <div class="instructions">
            <p>Use LEFT and RIGHT arrow keys to control engine thrust</p>
            <p>Left Engine: Pushes rocket RIGHT | Right Engine: Pushes rocket LEFT</p>
        </div>
        
        <div class="game-area" id="gameArea">
            <svg id="rocket" width="40" height="40" viewBox="0 0 40 40">
                <!-- Rocket body -->
                <rect x="15" y="5" width="10" height="25" fill="#e0e0e0" rx="2"/>
                <!-- Rocket nose -->
                <polygon points="15,5 25,5 20,0" fill="#f5f5f5"/>
                <!-- Rocket fins -->
                <polygon points="15,30 10,35 15,35" fill="#bdbdbd"/>
                <polygon points="25,30 30,35 25,35" fill="#bdbdbd"/>
                <!-- Cockpit window -->
                <circle cx="20" cy="12" r="3" fill="#4fc3f7"/>
            </svg>
            
            <div id="left-engine-flame"></div>
            <div id="right-engine-flame"></div>
            <div class="center-engine-flame" id="centerEngineFlame"></div>
            
            <div class="landing-pad"></div>
            <div class="landing-lights">
                <div class="landing-light"></div>
                <div class="landing-light"></div>
                <div class="landing-light"></div>
                <div class="landing-light"></div>
                <div class="landing-light"></div>
            </div>
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
        
        <div class="status" id="status">Altitude: 300ft | Speed: 15 mph | Angle: 0°</div>
    </div>
    
    <script>
        // Game variables
        let rocketX = 300;
        let rocketY = 50;
        let rocketAngle = 0;
        let velocityX = 0;
        let velocityY = 0.25; // Slow descent due to gravity
        let angularVelocity = 0;
        let altitude = 300;
        let speed = 15;
        let gameRunning = true;
        let lastThrustTime = 0;
        
        // DOM elements
        const rocket = document.getElementById('rocket');
        const leftFlame = document.getElementById('left-engine-flame');
        const rightFlame = document.getElementById('right-engine-flame');
        const centerFlame = document.getElementById('centerEngineFlame');
        const leftKey = document.getElementById('leftKey');
        const rightKey = document.getElementById('rightKey');
        const status = document.getElementById('status');
        const altitudeFill = document.getElementById('altitudeFill');
        const gameArea = document.getElementById('gameArea');
        const crashAnimation = document.getElementById('crashAnimation');
        const successAnimation = document.getElementById('successAnimation');
        
        // Initialize positions
        updateRocketPosition();
        
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
            const now = Date.now();
            if (now - lastThrustTime < 50) return; // Prevent spam
            lastThrustTime = now;
            
            leftKey.classList.add('active');
            leftFlame.style.opacity = '1';
            leftFlame.style.height = '40px';
            
            // Apply left thrust: pushes rocket RIGHT and creates CLOCKWISE rotation
            velocityX += 0.35;  // Push right
            angularVelocity += 1.0; // Clockwise rotation
            
            // Add slight wobble effect
            setTimeout(() => {
                if (leftKey.classList.contains('active')) {
                    rocketAngle += 0.5;
                }
            }, 50);
        }
        
        function deactivateLeftEngine() {
            leftKey.classList.remove('active');
            leftFlame.style.opacity = '0';
            leftFlame.style.height = '30px';
        }
        
        function activateRightEngine() {
            const now = Date.now();
            if (now - lastThrustTime < 50) return; // Prevent spam
            lastThrustTime = now;
            
            rightKey.classList.add('active');
            rightFlame.style.opacity = '1';
            rightFlame.style.height = '40px';
            
            // Apply right thrust: pushes rocket LEFT and creates COUNTER-CLOCKWISE rotation
            velocityX -= 0.35;  // Push left
            angularVelocity -= 1.0; // Counter-clockwise rotation
            
            // Add slight wobble effect
            setTimeout(() => {
                if (rightKey.classList.contains('active')) {
                    rocketAngle -= 0.5;
                }
            }, 50);
        }
        
        function deactivateRightEngine() {
            rightKey.classList.remove('active');
            rightFlame.style.opacity = '0';
            rightFlame.style.height = '30px';
        }
        
        function updateRocketPosition() {
            rocket.style.left = (rocketX - 20) + 'px';
            rocket.style.top = rocketY + 'px';
            rocket.style.transform = `rotate(${rocketAngle}deg)`;
            
            leftFlame.style.left = (rocketX - 25) + 'px';
            leftFlame.style.top = (rocketY + 35) + 'px';
            
            rightFlame.style.left = (rocketX + 5) + 'px';
            rightFlame.style.top = (rocketY + 35) + 'px';
            
            centerFlame.style.left = (rocketX - 12.5) + 'px';
            centerFlame.style.top = (rocketY + 35) + 'px';
        }
        
        function updateStatus() {
            status.textContent = `Altitude: ${Math.round(altitude)}ft | Speed: ${Math.round(speed)} mph | Angle: ${Math.round(rocketAngle)}°`;
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
            
            // Apply gravity for slow descent
            velocityY += 0.025;
            
            // Apply angular damping (natural stabilization)
            angularVelocity *= 0.97;
            rocketAngle += angularVelocity;
            
            // Apply air resistance for more realistic movement
            velocityX *= 0.985;
            velocityY *= 0.995;
            
            // Update position
            rocketX += velocityX;
            rocketY += velocityY;
            
            // Update altitude and speed
            altitude = 300 - rocketY;
            speed = Math.sqrt(velocityX * velocityX + velocityY * velocityY) * 12;
            
            // Boundary checks (allow some movement beyond edges)
            if (rocketX < -100) {
                showCrash();
                return;
            }
            if (rocketX > 700) {
                showCrash();
                return;
            }
            
            // Ground collision
            if (rocketY > 315) {
                rocketY = 315;
                velocityY = 0;
                
                // Check landing success
                if (Math.abs(rocketAngle) < 7 && Math.abs(velocityX) < 1.2) {
                    showSuccess();
                } else {
                    showCrash();
                }
            }
            
            // Update rocket position and status
            updateRocketPosition();
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
    print("🚀 Starting Realistic Rocket Landing Simulator...")
    print("🎮 Access the game at: http://localhost:8005")
    uvicorn.run(app, host="127.0.0.1", port=8005)