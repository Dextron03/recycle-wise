from django.shortcuts import render
from django.http import StreamingHttpResponse
from services.video.capturar_video import gen, VideoCamera

def home(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
