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
            const materialImage = document.getElementById('material-image');
            detectionsList.innerHTML = '';  // Borrar contenido anterior

            if (Array.isArray(data) && data.length > 0) {
                data.forEach(detection => {
                    const materialItem = document.createElement('li');
                    materialItem.textContent = `Material: ${detection.class}`;

                    const confidenceItem = document.createElement('li');
                    confidenceItem.textContent = `Percentage: ${detection.confidence}%`;

                    detectionsList.appendChild(materialItem);
                    detectionsList.appendChild(confidenceItem);

                    // Construir la ruta de la imagen
                    const newSrc = `static/imgs/${detection.class}.png`;
                    console.log(`Cambiando imagen a: ${newSrc}`);
                    
                    // Actualizar el src de la imagen según el material
                    materialImage.src = newSrc;
                });
            } else {
                const materialItem = document.createElement('li');
                materialItem.textContent = `Material: ...`;

                const confidenceItem = document.createElement('li');
                confidenceItem.textContent = `Percentage: ...`;

                detectionsList.appendChild(materialItem);
                detectionsList.appendChild(confidenceItem);

                console.error('No se detectaron objetos o los datos de detecciones no son una matriz');
                // Volver a la imagen por defecto
                materialImage.src = 'static/imgs/default.png';
            }
        })
        .catch(error => {
            console.error('Error al obtener detecciones:', error);
            // Volver a la imagen por defecto en caso de error
            const materialImage = document.getElementById('material-image');
            materialImage.src = '{% static "imgs/default.png" %}';
        });
}

document.addEventListener('DOMContentLoaded', () => {
    setInterval(fetchDetections, 1000);
});
