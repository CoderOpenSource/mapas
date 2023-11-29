from django.conf import settings
from django.db import models
from ..usuarios.models import Cliente
class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    año = models.CharField(max_length=4)
    foto = models.ImageField(upload_to='vehiculos/', null=True, blank=True)

    # Otros campos...
