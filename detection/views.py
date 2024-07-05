# views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from services.video.capturar_video import generate_frame, VideoCamera

# Inicializa la cámara de video
camera = VideoCamera(camera_index=0)

def home(request):
    """
    Renderiza la página principal.

    Esta vista maneja la solicitud HTTP para la página principal de la aplicación.
    Toma el objeto de la solicitud HTTP como parámetro y retorna una respuesta HTTP
    que contiene el contenido de la plantilla 'index.html'. La función renderiza 
    esta plantilla y la devuelve como respuesta.
    
    Retorna:
    - HttpResponse: La respuesta HTTP con el contenido de 'index.html'.
    """
    
    return render(request, 'index.html')

def video_feed(request):
    """
    Proporciona el stream de video de la cámara.

    Esta vista maneja la solicitud HTTP para el stream de video. Utiliza la 
    función generate_frame para capturar y procesar los frames de video en 
    tiempo real. La respuesta HTTP es un StreamingHttpResponse que contiene 
    el stream de video, con el tipo de contenido adecuado para la transmisión 
    de video en múltiples partes.
    
    Retorna:
    - StreamingHttpResponse: La respuesta HTTP que contiene el stream de video.
    """
    
    return StreamingHttpResponse(generate_frame(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def get_detections(request):
    """
    Devuelve las detecciones actuales de objetos en formato JSON.

    Esta vista maneja la solicitud HTTP para obtener las detecciones actuales 
    de objetos. La función obtiene las detecciones desde la cámara y las 
    devuelve en una respuesta JSON. Esto permite a otras partes de la 
    aplicación (como el frontend) acceder a los datos de detección en un 
    formato estructurado y fácil de usar.

    Parámetros:
    - request (HttpRequest): El objeto de la solicitud HTTP.
    
    Retorna:
    - JsonResponse: La respuesta HTTP en formato JSON que contiene las detecciones.
    """
    
    detections = camera.get_detections()
    return JsonResponse(detections, safe=False)
