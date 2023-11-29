# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudAsistenciaViewSet, ImagenSolicitudViewSet, PostulacionViewSet

router = DefaultRouter()
router.register(r'solicitudes-asistencia', SolicitudAsistenciaViewSet)
router.register(r'imagenes-solicitud', ImagenSolicitudViewSet)
router.register(r'postulaciones', PostulacionViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
