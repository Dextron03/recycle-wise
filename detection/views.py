# views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from services.video.capturar_video import generate_frame, VideoCamera

camera = VideoCamera(camera_index=2)

def home(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frame(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def get_detections(request):
    detections = camera.get_detections()
    return JsonResponse(detections, safe=False)
