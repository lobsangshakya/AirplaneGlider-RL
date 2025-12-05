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
let windY = 0;
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
    windX = 150;
    windY = 0;
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
        
        // Collision check
        let planeRect = plane.getBoundingClientRect();
        let windRect = wind.getBoundingClientRect();
        
        // More accurate collision detection
        if (planeRect.left < windRect.right && 
            planeRect.right > windRect.left && 
            planeRect.top < windRect.bottom && 
            planeRect.bottom > windRect.top) {
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
        
        // Reset wind
        if (windY > 600) {
            windY = -40;
            wind.style.top = windY + "px";
            windX = Math.floor(Math.random() * 350);
            wind.style.left = windX + "px";
        }
    }, 100);
}

// Add event listener to button
startButton.addEventListener("click", startGame);