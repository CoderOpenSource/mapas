from django.db import models

# Create your models here.
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ..usuarios.models import Cliente


class CalificacionesResenas(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reseñas_dadas')

    # Para manejar la relación polimórfica con Taller o Técnico:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    puntuacion = models.PositiveIntegerField(help_text="Puntuación dada, por ejemplo, de 1 a 5")
    comentario = models.TextField()

    # Puedes añadir más campos aquí si lo necesitas

    def __str__(self):
        return f"Reseña por {self.usuario.user.username} para {self.content_type.model}"

    class Meta:
        verbose_name_plural = "Calificaciones y Reseñas"
