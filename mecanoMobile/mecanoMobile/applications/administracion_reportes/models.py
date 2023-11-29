from django.db import models

from applications.usuarios.models import Cliente, Tecnico, Taller


# Create your models here.
class HistorialServicios(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historial_servicios')
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='servicios_realizados')
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='servicios_proveidos')
    fecha_servicio = models.DateField(verbose_name='Fecha del Servicio')
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Servicio {self.id} para Usuario {self.usuario.user.username}"
