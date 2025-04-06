let chart;

function getRandomValue(min, max) {
  return (Math.random() * (max - min) + min).toFixed(2);
}

function updateValues() {
  const boxes = document.querySelectorAll('.sensor-box');

  boxes.forEach((box, index) => {
    const value = parseFloat(getRandomValue(-100, 100));
    const change = parseFloat(getRandomValue(-10, 10));

    const valueElem = box.querySelector('.sensor-value');
    const changeElem = box.querySelector('.sensor-change');

    valueElem.textContent = `${value}`;
    changeElem.textContent = `${change}`;

    // Set color based on value
    changeElem.classList.remove('text-green', 'text-red', 'text-yellow');
    if (isNaN(change) || change === 0) {
      changeElem.classList.add('text-yellow');
    } else if (change < 0) {
      changeElem.classList.add('text-red');
    } else {
      changeElem.classList.add('text-green');
    }
  });

  updateGraph();
}

function updateGraph() {
  const labels = [];
  const dataPoints = [];

  document.querySelectorAll('.sensor-box').forEach((box, index) => {
    const title = box.querySelector('.sensor-title')?.textContent || `Sensor ${index + 1}`;
    const valueText = box.querySelector('.sensor-value')?.textContent || '0';
    const value = parseFloat(valueText.replace(/[^\d.-]/g, ''));

    labels.push(title);
    dataPoints.push(isNaN(value) ? 0 : value);
  });

  const ctx = document.getElementById('sensorGraph').getContext('2d');

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
          label: '', // Removed "Sensor Values" label
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
            display: false // Hide legend
          },
          title: {
            display: false // Hide chart title
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

setInterval(updateValues, 10000);

window.onload = updateValues;

function updateDateTime() {
  const now = new Date();

  // Format: 5 April 2025
  const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };
  const dateString = now.toLocaleDateString('en-GB', dateOptions);

  const timeString = now.toLocaleTimeString();

  document.getElementById('datetime').textContent = `${dateString}, ${timeString}`;
}

// Call once initially and then every second
updateDateTime();
setInterval(updateDateTime, 1000);
