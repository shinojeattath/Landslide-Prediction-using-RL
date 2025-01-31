// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeBackgrounds();
    initializeLoader();
    
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

function initializeBackgrounds() {
    const times = ['morning', 'evening', 'night'];
    let currentIndex = 0;
    
    const container = document.createElement('div');
    container.className = 'background-container';
    document.body.appendChild(container);
    
    times.forEach(time => {
        const overlay = document.createElement('div');
        overlay.className = `overlay ${time}`;
        container.appendChild(overlay);
    });

    function changeBackground() {
        const overlays = document.querySelectorAll('.overlay');
        const images = document.querySelectorAll('.background-image');
        
        overlays.forEach(overlay => overlay.style.opacity = '0');
        images.forEach(img => img.style.opacity = '0');
        
        overlays[currentIndex].style.opacity = '1';
        images[currentIndex].style.opacity = '1';

        document.body.setAttribute('data-time', times[currentIndex]);
        
        currentIndex = (currentIndex + 1) % times.length;
    }

    setInterval(changeBackground, 10000);
    changeBackground();
}

function initializeLoader() {
    setTimeout(() => {
        const loader = document.querySelector('.loader');
        const loaderContainer = document.querySelector('.loader-container');
        const contentContainer = document.querySelector('.content-container');
        
        if (loader && loaderContainer) {
            loader.classList.add('expand');

            setTimeout(() => {
                loaderContainer.style.opacity = '0';
                if (contentContainer) contentContainer.style.opacity = '1';
                setTimeout(() => {
                    loaderContainer.style.display = 'none';
                }, 500);
            }, 1000);
        }
    }, 2000);
}

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