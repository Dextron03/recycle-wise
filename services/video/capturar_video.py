import cv2
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            raise Exception("No se pudo abrir el dispositivo de video.")
        (self.grabbed, self.frame) = self.video.read()
        if not self.grabbed:
            raise Exception("No se pudo leer el cuadro del dispositivo de video.")
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if not self.grabbed:
                print("Frame grab failed")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

