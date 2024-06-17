from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from services.video.capturar_video import gen, VideoCamera

camera = VideoCamera(camera_index=0)

def home(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def get_detections(request):
    detections = camera.get_detections()
    return JsonResponse(detections, safe=False)
