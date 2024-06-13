from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from services.video.capturar_video import VideoCamera, gen

@gzip.gzip_page
def Home(request):
    return render(request, 'index.html')

def video_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return HttpResponse(status=500)
