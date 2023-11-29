from django.db import models
from ..usuarios.models import Cliente, Taller, Tecnico
from django.contrib.gis.db import models as gis_models

class SolicitudAsistencia(models.Model):
    TIPOS_PROBLEMAS = (
        ('bateria', 'Problemas con la batería'),
        ('llanta_pinchada', 'Se pincha alguna llanta'),
        ('sin_combustible', 'El vehículo se queda sin combustible'),
        ('no_arranca', 'El vehículo no arranca'),
        ('pierde_llave', 'Perder la llave del vehículo'),
        ('llave_adentro', 'Dejar llave dentro del vehículo'),
        ('otros', 'Otros'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='solicitudes')
    ubicacion = gis_models.PointField(srid=4326,null=True)  # srid=4326 es el sistema de referencia espacial comúnmente usado para latitud/longitud.
    tipo_problema = models.CharField(max_length=255, choices=TIPOS_PROBLEMAS)
    descripcion = models.TextField()
    audio = models.CharField(max_length=255, null=True, blank=True)
    taller_aceptado = models.ForeignKey(Taller, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='solicitudes_aceptadas')
    tecnico_asignado = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='solicitudes_atendidas')

    def __str__(self):
        return f"Solicitud {self.id} por {self.cliente.user.username}"

class ImagenSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudAsistencia, on_delete=models.CASCADE, related_name='imagenes')
    foto = models.ImageField(upload_to='solicitudes/', null=True, blank=True)

    def __str__(self):
        return f"Imagen {self.id} para Solicitud {self.solicitud.id}"

class Postulacion(models.Model):
    ESTADOS_POSTULACION = (
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    )

    solicitud = models.ForeignKey(
        SolicitudAsistencia,
        on_delete=models.CASCADE,
        related_name='postulaciones'
    )
    taller = models.ForeignKey(
        Taller,
        on_delete=models.CASCADE,
        related_name='postulaciones'
    )
    tiempo_estimado = models.CharField(
        max_length=50,
        verbose_name='Tiempo Estimado',
        help_text='Tiempo estimado para completar la asistencia.'
    )
    distancia_estimada = models.CharField(
        max_length=50,
        verbose_name='Distancia Estimada',
        help_text='Distancia Estimada para completar la asistencia.',
        null=False,
        default='1'
    )
    costo_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Estimado',
        help_text='Costo estimado para la asistencia.'
    )
    estado_postulacion = models.CharField(
        max_length=10,
        choices=ESTADOS_POSTULACION,
        default='pendiente',
        verbose_name='Estado de la Postulación'
    )
    comentarios = models.TextField(
        blank=True,
        null=True,
        verbose_name='Comentarios',
        help_text='Comentarios adicionales sobre la postulación.'
    )

    def __str__(self):
        return f"Postulación {self.id} por {self.taller.nombre} para Solicitud {self.solicitud.id}"

class OrdenTrabajo(models.Model):
    ESTADOS_ORDEN = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    solicitud = models.ForeignKey(
        SolicitudAsistencia,
        on_delete=models.CASCADE,
        related_name='ordenes'
    )
    tecnico = models.ForeignKey(
        Tecnico,
        on_delete=models.CASCADE,
        related_name='ordenes_asignadas'
    )
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio')
    fecha_final = models.DateTimeField(verbose_name='Fecha de Finalización', null=True, blank=True)
    estado_orden = models.CharField(
        max_length=15,
        choices=ESTADOS_ORDEN,
        default='pendiente',
        verbose_name='Estado de la Orden'
    )
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden de Trabajo {self.id} para Solicitud {self.solicitud.id}"
