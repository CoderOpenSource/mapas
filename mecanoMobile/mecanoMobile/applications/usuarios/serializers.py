from rest_framework import serializers
from .models import Cliente, Taller, Tecnico, CustomUser
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import make_password

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'



class TallerSerializer(serializers.ModelSerializer):
    latitud = serializers.FloatField(write_only=True, required=False)
    longitud = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Taller
        fields = '__all__'  # Agrega 'latitud' y 'longitud' como campos para escritura.
        read_only_fields = ('ubicacion',)  # El campo 'ubicacion' es de sólo lectura.

    def create(self, validated_data):
        # Extrae latitud y longitud y los elimina de validated_data
        latitud = validated_data.pop('latitud', None)
        longitud = validated_data.pop('longitud', None)
        # Crea la instancia de Taller normalmente
        taller = Taller.objects.create(**validated_data)
        # Si se proporcionaron latitud y longitud, actualiza el campo 'ubicacion'
        if latitud is not None and longitud is not None:
            taller.ubicacion = Point(longitud, latitud)
            taller.save()
        return taller

    def update(self, instance, validated_data):
        # Extrae latitud y longitud y los elimina de validated_data
        latitud = validated_data.pop('latitud', None)
        longitud = validated_data.pop('longitud', None)
        # Actualiza la instancia de Taller normalmente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Si se proporcionaron latitud y longitud, actualiza el campo 'ubicacion'
        if latitud is not None and longitud is not None:
            instance.ubicacion = Point(longitud, latitud)
            instance.save()
        return instance

    def to_representation(self, instance):
        """Transforma el objeto en un diccionario de datos."""
        ret = super().to_representation(instance)
        ret['latitud'] = instance.ubicacion.y if instance.ubicacion else None
        ret['longitud'] = instance.ubicacion.x if instance.ubicacion else None
        return ret


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    # Modificamos el campo user_type para excluir la opción 'admin'
    user_type = serializers.ChoiceField(choices=[(choice[0], choice[1]) for choice in CustomUser.USER_TYPE_CHOICES if choice[0] != 1])
    # Añade el campo de contraseña, permitiendo escribir pero no leer
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'email', 'password', 'user_type', 'first_name', 'foto')

    # Sobrescribe el método create para manejar el almacenamiento seguro de la contraseña
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            user_type=validated_data['user_type'],  # Aquí hemos agregado el user_type
        )
        user.set_password(validated_data['password'])
        # Añadir foto si está disponible en validated_data
        foto = validated_data.get('foto', None)
        if foto is not None:
            user.foto = foto
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        if 'foto' in validated_data:
            instance.foto = validated_data.get('foto', instance.foto)

        # Comprobar si la contraseña está presente en los datos validados
        password = validated_data.pop('password', None)
        if password is not None:
            # Hashear la nueva contraseña antes de guardarla
            instance.password = make_password(password)

        # Guarda el objeto de usuario actualizado
        instance.save()
        return instance
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    fcm_token = serializers.CharField(write_only=True, required=False)  # Opcional
