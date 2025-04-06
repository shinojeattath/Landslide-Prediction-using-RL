// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Make the evaluate function globally available
    window.evaluateLandslide = function() {
        console.log("Evaluate function called");
        fetch('/predict/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerText = data.prediction;
            })
            .catch(error => console.error('Error:', error));
    };

    // Start periodic prediction updates
    setInterval(evaluateLandslide, 10000);
});





//Timer
document.addEventListener('DOMContentLoaded', function() {
    // Initialize countdown and prediction
    startCountdown();
    evaluateLandslide();

    // Make the evaluate function globally available
    window.evaluateLandslide = function() {
        console.log("Evaluate function called");
        fetch('/predict/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerText = data.prediction;
                startCountdown(); // Restart countdown after prediction
            })
            .catch(error => {
                console.error('Error:', error);
                startCountdown(); // Restart countdown even if there's an error
            });
    };
});

function startCountdown() {
    let timeLeft = 10;
    const timerDisplay = document.getElementById('timer');
    
    // Clear any existing interval
    if (window.countdownInterval) {
        clearInterval(window.countdownInterval);
    }
    
    // Update the countdown every second
    window.countdownInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(window.countdownInterval);
            evaluateLandslide();
        }
    }, 1000);
}