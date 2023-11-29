from django.db import models

from applications.usuarios.models import CustomUser


# Create your models here.
class Notificaciones(models.Model):
    TIPOS_NOTIFICACION = (
        ('solicitud_asistencia', 'Solicitud de Asistencia'),
        ('confirmacion_pago', 'Confirmación de Pago'),
        # ... otros tipos según sea necesario
    )
    ESTADOS_NOTIFICACION = (
        ('no_leido', 'No Leído'),
        ('leido', 'Leído'),
    )

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30, choices=TIPOS_NOTIFICACION)
    estado_notificacion = models.CharField(max_length=10, choices=ESTADOS_NOTIFICACION, default='no_leido')

    def __str__(self):
        return f"Notificación para {self.usuario.username}"
