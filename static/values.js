// values.js - Updated for Django integration
let chart;
let previousValues = {
    temp: 0,
    humidity: 0,
    soil: 0,
    rain: 'Low',
    accelX: 0,
    accelY: 0,
    accelZ: 0,
    pressure: 0
};

// Function to fetch sensor data from Django backend
function fetchSensorData() {
    fetch('/api/sensor-data/')
        .then(response => response.json())
        .then(data => {
            updateSensorValues(data.current);
            updateGraph(data.current);
            console.log("data fetched successfully", data)
        })
        .catch(error => {
            console.error('Error fetching sensor data:', error);
            // If API fails, use random data for demonstration
            //useRandomData();
        });
}

// Function to update sensor values with real data
function updateSensorValues(sensorData) {
    // Temperature
    const temp = sensorData.temperature.toFixed(1);
    const tempChange = calculatePercentChange(temp, previousValues.temp);
    document.getElementById('temp').textContent = `${temp} °C`;
    updateChangeElement('temp-change', tempChange);
    previousValues.temp = parseFloat(temp);
    
    // Humidity
    const humidity = sensorData.humidity.toFixed(1);
    const humidityChange = calculatePercentChange(humidity, previousValues.humidity);
    document.getElementById('humidity').textContent = `${humidity} %`;
    updateChangeElement('humidity-change', humidityChange);
    previousValues.humidity = parseFloat(humidity);
    
    // Soil Moisture
    const soil = sensorData.soil_moisture;
    const soilChange = calculatePercentChange(soil, previousValues.soil);
    document.getElementById('soil').textContent = soil;
    updateChangeElement('soil-change', soilChange);
    previousValues.soil = soil;
    
    // Rain - Derive from humidity or use default if not available
    const rain = deriveRainStatus(sensorData.rainfall || sensorData.humidity);
    document.getElementById('rain').textContent = rain;
    document.getElementById('rain-change').textContent = '-';
    previousValues.rain = rain;
    
    // Acceleration
    const accelX = sensorData.accel_x.toFixed(2);
    const accelY = sensorData.accel_y.toFixed(2);
    const accelZ = sensorData.accel_z.toFixed(2);
    document.getElementById('accel').textContent = `X: ${accelX} | Y: ${accelY} | Z: ${accelZ}`;
    document.getElementById('accel-change').textContent = '-';
    previousValues.accelX = parseFloat(accelX);
    previousValues.accelY = parseFloat(accelY);
    previousValues.accelZ = parseFloat(accelZ);
    
    // Pressure
    const pressure = (sensorData.pressure / 100).toFixed(1); // Convert Pa to hPa
    const pressureChange = calculatePercentChange(pressure, previousValues.pressure);
    document.getElementById('pressure').textContent = `${pressure} hPa`;
    updateChangeElement('pressure-change', pressureChange);
    previousValues.pressure = parseFloat(pressure);
    
    // Update risk level indicator if it exists
    if (sensorData.risk_level !== undefined && document.getElementById('risk-indicator')) {
        updateRiskIndicator(sensorData.risk_level);
    }
}

// Helper function to calculate percent change
function calculatePercentChange(current, previous) {
    if (!previous) return 0;
    return ((current - previous) / previous * 100).toFixed(1);
}

// Helper function to update change element with color coding
function updateChangeElement(elementId, changeValue) {
    const element = document.getElementById(elementId);
    element.textContent = `${changeValue > 0 ? '+' : ''}${changeValue}% from avg`;
    
    // Set color based on change
    element.classList.remove('text-green', 'text-red', 'text-yellow');
    if (changeValue == 0) {
        element.classList.add('text-yellow');
    } else if (changeValue < 0) {
        element.classList.add('text-red');
    } else {
        element.classList.add('text-green');
    }
}

// Helper function to determine rain status based on humidity
function deriveRainStatus(humidityOrRain) {
    if (typeof humidityOrRain === 'string') {
        return humidityOrRain; // Already a status
    }
    
    // Use humidity to estimate rain status
    if (humidityOrRain > 90) return 'High';
    if (humidityOrRain > 75) return 'Medium';
    return 'Low';
}

// Function to update risk indicator if it exists
function updateRiskIndicator(riskLevel) {
    const riskIndicator = document.getElementById('risk-indicator');
    if (!riskIndicator) return;
    
    if (riskLevel === 1) {
        riskIndicator.classList.remove('status-safe');
        riskIndicator.classList.add('status-danger');
        riskIndicator.textContent = 'WARNING! LANDSLIDE RISK DETECTED';
    } else {
        riskIndicator.classList.remove('status-danger');
        riskIndicator.classList.add('status-safe');
        riskIndicator.textContent = 'TERRAIN STABLE - NO RISK DETECTED';
    }
}

// Function to update the chart with real data
function updateGraph(sensorData) {
    const ctx = document.getElementById('sensorGraph').getContext('2d');
    
    const labels = ['Temperature', 'Humidity', 'Soil Moisture', 'Pressure', 'Slope'];
    const dataPoints = [
        sensorData.temperature,
        sensorData.humidity,
        sensorData.soil_moisture,
        sensorData.pressure / 100, // Convert Pa to hPa
        sensorData.slope || 0
    ];
    
    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = dataPoints;
        chart.update();
    } else {
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '',
                    data: dataPoints,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Fallback function to use random data if API fails
function useRandomData() {
    const getRandomValue = (min, max) => (Math.random() * (max - min) + min).toFixed(1);
    
    const mockData = {
        temperature: parseFloat(getRandomValue(20, 30)),
        humidity: parseFloat(getRandomValue(40, 80)),
        pressure: parseFloat(getRandomValue(90000, 102000)),
        altitude: parseFloat(getRandomValue(100, 500)),
        accel_x: parseFloat(getRandomValue(-1, 1)),
        accel_y: parseFloat(getRandomValue(-1, 1)),
        accel_z: parseFloat(getRandomValue(8, 10)),
        soil_moisture: parseInt(getRandomValue(300, 700)),
        rainfall: 0,
        slope: parseFloat(getRandomValue(0, 20)),
        risk_level: Math.random() > 0.8 ? 1 : 0
    };
    
    updateSensorValues(mockData);
    updateGraph(mockData);
}

function updateDateTime() {
    const now = new Date();
    const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };
    const dateString = now.toLocaleDateString('en-GB', dateOptions);
    const timeString = now.toLocaleTimeString();
    
    document.getElementById('datetime').textContent = `${dateString}, ${timeString}`;
}

// Fetch sensor data every 10 seconds
setInterval(fetchSensorData, 2000);

// Update date and time every second
setInterval(updateDateTime, 1000);

// Initialize on page load
window.onload = function() {
    fetchSensorData();
    updateDateTime();
};