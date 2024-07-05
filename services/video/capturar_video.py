import cv2
import threading
import math
from ultralytics import YOLO

# Definir el modelo YOLO y las clases de detección
model = YOLO('modelos/best.pt')
class_names = ['Metal', 'Vidrio', 'Plastico', 'Carton', 'Medicinal']

class VideoCamera(object):
    def __init__(self, camera_index=0):  # Cambiar a 2 para usar DroidCam y 0 para la cámara por defecto
        """
        Inicializa la cámara de video.
        
        Parámetros:
        - camera_index (int): Índice de la cámara a utilizar. 0 para la cámara por defecto, 2 para DroidCam.
        
        Acciones:
        - Configura la resolución de la cámara.
        - Inicia un hilo para actualizar los frames de la cámara continuamente.
        """
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.video.set(3, 1280)
        self.video.set(4, 720)
        (self.grabbed, self.frame) = self.video.read()
        self.lock = threading.Lock()
        self.detections = []
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        """ Libera la cámara cuando el objeto es destruido. """
        self.video.release()

    def get_frame(self):
        """
        Captura un frame de la cámara y realiza la detección de objetos.
        
        Retorna:
        - jpeg (bytes): El frame procesado en formato JPEG.
        
        Acciones:
        - Captura un frame de la cámara.
        - Realiza detección de objetos en el frame usando el modelo YOLO.
        - Dibuja rectángulos y etiquetas sobre los objetos detectados.
        - Convierte el frame procesado a formato JPEG.
        """
        with self.lock:
            image = self.frame.copy()
        results = model(image, stream=True, verbose=False)
        temp_detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1, y1, x2, y2 = max(0, x1), max(0, y1), max(0, x2), max(0, y2)
                cls = int(box.cls[0])
                confidence = math.ceil(box.conf[0] * 100)

                if confidence > 0:
                    temp_detections.append({'class': class_names[cls], 'confidence': confidence})
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(image, f'{class_names[cls]} {confidence}%', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        with self.lock:
            self.detections = temp_detections
        
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_detections(self):
        """
        Obtiene las detecciones actuales de objetos.
        
        Retorna:
        - detections (list): Lista de diccionarios con las detecciones actuales.
        
        Acciones:
        - Devuelve una copia de las detecciones actuales almacenadas en el objeto.
        """
        with self.lock:
            return self.detections if self.detections else []

    def update(self):
        """
        Actualiza continuamente los frames de la cámara en un hilo separado.
        
        Acciones:
        - Captura frames de la cámara en un bucle infinito y actualiza la variable `self.frame`.
        """
        while True:
            (self.grabbed, self.frame) = self.video.read()
            with self.lock:
                self.frame = self.frame

def generate_frame(camera: VideoCamera):
    """
    Genera un stream continuo de frames JPEG.
    
    Parámetros:
    - camera (VideoCamera): Objeto VideoCamera para capturar los frames.
    
    Retorna:
    - frame (bytes): Stream continuo de frames JPEG con el formato requerido para la transmisión HTTP.
    
    Acciones:
    - Captura y codifica continuamente los frames de la cámara en formato JPEG.
    - Formatea los frames para la transmisión HTTP.
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
