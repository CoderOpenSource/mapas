from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, TallerViewSet, TecnicoViewSet, CustomUserViewSet, LoginView

# Instancia del enrutador por defecto
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'talleres', TallerViewSet)
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'users', CustomUserViewSet)

# Patrones de URL
urlpatterns = [
    *router.urls, # Incluye todas las URL de los ViewSets registrados en el enrutador
    path('login/', LoginView.as_view(), name='login'),  # Ruta para la vista de login
]
