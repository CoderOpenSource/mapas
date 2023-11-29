# Generated by Django 4.2.6 on 2023-11-01 16:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_cliente_foto_taller_foto_tecnico_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudAsistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('tipo_problema', models.CharField(choices=[('bateria', 'Problemas con la batería'), ('llanta_pinchada', 'Se pincha alguna llanta'), ('sin_combustible', 'El vehículo se queda sin combustible'), ('no_arranca', 'El vehículo no arranca'), ('pierde_llave', 'Perder la llave del vehículo'), ('llave_adentro', 'Dejar llave dentro del vehículo'), ('otros', 'Otros')], max_length=255)),
                ('descripcion', models.TextField()),
                ('audio', models.FileField(blank=True, null=True, upload_to='audios/')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='usuarios.cliente')),
                ('taller_aceptado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes_aceptadas', to='usuarios.taller')),
                ('tecnico_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes_atendidas', to='usuarios.tecnico')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='solicitudes/')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='solicitudes_asistencia.solicitudasistencia')),
            ],
        ),
    ]
