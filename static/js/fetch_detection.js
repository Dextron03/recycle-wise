function fetchDetections() {
    fetch(" get_detections")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const detectionsList = document.getElementById('detections-list');
            detectionsList.innerHTML = '';
            if (Array.isArray(data)) {
                data.forEach(detection => {
                    const li = document.createElement('li');
                    li.textContent = `${detection.class}: ${detection.confidence}%`;
                    detectionsList.appendChild(li);
                });
            } else {
                console.error('Detections data is not an array or is null');
            }
        })
        .catch(error => console.error('Error fetching detections:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    setInterval(fetchDetections, 1000);
});
