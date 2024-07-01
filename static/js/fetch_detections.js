function fetchDetections() {
    fetch("get_detections")
        .then(response => {
            if (!response.ok) {
                throw new Error('La respuesta de la red no fue correcta ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const detectionsList = document.getElementById('detections-list');
            detectionsList.innerHTML = '';  // Borrar contenido anterior

            if (Array.isArray(data)) {
                data.forEach(detection => {
                    const materialItem = document.createElement('li');
                    materialItem.textContent = `Material: ${detection.class}`;

                    const confidenceItem = document.createElement('li');
                    confidenceItem.textContent = `Percentage: ${detection.confidence}%`;

                    detectionsList.appendChild(materialItem);
                    detectionsList.appendChild(confidenceItem);
                });
            } else {
                console.error('Los datos de detecciones no son una matriz o son nulos');
            }
        })
        .catch(error => console.error('Error al obtener detecciones:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    setInterval(fetchDetections, 1000);
});
