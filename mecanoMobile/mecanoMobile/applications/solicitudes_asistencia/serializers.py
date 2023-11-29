from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import SolicitudAsistencia, ImagenSolicitud, Postulacion

class ImagenSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenSolicitud
        fields = '__all__'

class SolicitudAsistenciaSerializer(serializers.ModelSerializer):
    latitud = serializers.FloatField(write_only=True, required=False)
    longitud = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = SolicitudAsistencia
        fields = '__all__'
        read_only_fields = ('ubicacion',)

    def create(self, validated_data):
        latitud = validated_data.pop('latitud', None)
        longitud = validated_data.pop('longitud', None)

        solicitud = SolicitudAsistencia.objects.create(**validated_data)

        if latitud is not None and longitud is not None:
            solicitud.ubicacion = Point(longitud, latitud)
            solicitud.save()

        return solicitud

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['latitud'] = instance.ubicacion.y if instance.ubicacion else None
        ret['longitud'] = instance.ubicacion.x if instance.ubicacion else None
        return ret

class PostulacionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Postulacion
            fields = '__all__'