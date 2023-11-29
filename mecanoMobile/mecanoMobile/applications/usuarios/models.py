from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.gis.db import models as gis_models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'cliente'),
        (3, 'taller'),
        (4, 'tecnico'),
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    foto = models.ImageField(upload_to='users/', null=True, blank=True)  # Campo foto agregado aquí

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="customuser_groups",
        verbose_name=("groups")
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name="customuser_user_permissions",
        verbose_name=("user permissions")
    )

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        group_name = ""
        if self.user_type == 1:
            group_name = 'Admin'
        elif self.user_type == 2:
            group_name = 'Cliente'
        elif self.user_type == 3:
            group_name = 'Taller'
        elif self.user_type == 4:
            group_name = 'Tecnico'

        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)



class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    # Otros campos específicos para el cliente si es necesario


class Taller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, default='Desconocido')  # Nombre y dirección física del taller
    ubicacion = gis_models.PointField(srid=4326, null=True, blank=True)
    hora_apertura = models.TimeField(default='08:00:00')  # Por ejemplo, 8 AM como default
    hora_cierre = models.TimeField(default='17:00:00')  # Por ejemplo, 5 PM como default

    # Otros campos específicos para el taller si es necesario

    def esta_abierto_hoy(self):
        hoy = datetime.now().time()
        dia_semana = datetime.now().strftime('%A').lower()  # esto nos da el día de la semana en español

        if dia_semana == 'domingo':
            return False  # si es domingo, asumimos que está cerrado
        return self.hora_apertura <= hoy <= self.hora_cierre

    def __str__(self):
        return self.nombre


class Tecnico(models.Model):
    ESPECIALIDADES = (
        ('mecanico_general', 'Mecánico General'),
        ('electrico', 'Eléctrico'),
        ('tornero', 'Tornero'),
        # Las opciones existentes
        ('pintor', 'Pintor'),
        ('chapista', 'Chapista'),
        # La nueva opción añadida
        ('gomero', 'Gomero'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, related_name='tecnicos', on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=255, choices=ESPECIALIDADES)

    def __str__(self):
        return f"{self.user.username} - {self.get_especialidad_display()}"
