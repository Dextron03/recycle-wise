from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_detections/', views.get_detections, name='get_detections'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
