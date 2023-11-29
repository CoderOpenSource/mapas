from django.db import models

from applications.usuarios.models import CustomUser
class Comunicaciones(models.Model):
    ESTADOS_MENSAJE = (
        ('no_leido', 'No Leído'),
        ('leido', 'Leído'),
    )

    emisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    mensaje = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado_mensaje = models.CharField(max_length=10, choices=ESTADOS_MENSAJE, default='no_leido')

    def __str__(self):
        return f"Mensaje de {self.emisor.username} a {self.receptor.username}"
