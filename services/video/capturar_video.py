import cv2
import threading
import math
from ultralytics import YOLO

# Definir el modelo YOLO y las clases de detección
model = YOLO('modelos/best.pt')
class_names = ['Metal', 'Vidrio', 'Plastico', 'Carton', 'Medicinal']

class VideoCamera(object):
    def __init__(self, camera_index=0):  # Cambiar a 2 para usar DroidCam y 0 para la cámara por defecto
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.video.set(3, 1280)
        self.video.set(4, 720)
        (self.grabbed, self.frame) = self.video.read()
        self.lock = threading.Lock()
        self.detections = []
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
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
        with self.lock:
            return self.detections if self.detections else []

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            with self.lock:
                self.frame = self.frame

def generate_frame(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
