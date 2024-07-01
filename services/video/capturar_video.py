
import cv2
import threading
import math
from ultralytics import YOLO

# Definir el modelo YOLO y las clases
model = YOLO('modelos/best.pt')
clsName = ['Metal', 'Vidrio', 'Plastico', 'Carton', 'Medical']

class VideoCamera(object):
    def __init__(self, camera_index=0):  # Cambiar a 2 para usar DroidCam y 0 para la camara por defecto
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
        detections = []

        for res in results:
            for box in res.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1, y1, x2, y2 = max(0, x1), max(0, y1), max(0, x2), max(0, y2)
                cls = int(box.cls[0])
                conf = math.ceil(box.conf[0] * 100)

                if conf > 0:
                    detections.append({'class': clsName[cls], 'confidence': conf})
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(image, f'{clsName[cls]} {conf}%', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        with self.lock:
            self.detections = detections
        
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_detections(self):
        with self.lock:
            if self.detections:
                return self.detections
            else:
                return []

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            with self.lock:
                self.frame = self.frame

def gen(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
