from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from fcm_django.models import FCMDevice
from .models import SolicitudAsistencia, ImagenSolicitud, Postulacion
from .serializers import SolicitudAsistenciaSerializer, ImagenSolicitudSerializer, PostulacionSerializer
from firebase_admin import messaging
from cloudinary.uploader import upload
class SolicitudAsistenciaViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAsistencia.objects.all()
    serializer_class = SolicitudAsistenciaSerializer

    def subir_audio_a_cloudinary(self, archivo_audio):
        # Utiliza las credenciales de API de Cloudinary desde tus ajustes de Django
        try:
            resultado = upload(
                archivo_audio,
                cloud_name= "dkpuiyovk",
                api_key="469764952158318",
                api_secret="Za0rsohDusweXFfpyjCiFPUgzug",
                resource_type="raw"  # Cambiado a 'raw' para archivos de audio
            )
            return resultado.get('url')
        except Exception as e:
            print(f"Error al subir a Cloudinary: {e}")
            return None  # Retorna None si hay algún problema con la carga

    def create(self, request, *args, **kwargs):
        print("Datos recibidos (POST):", request.POST)
        print("Archivos recibidos:", request.FILES)

        # Procesar el archivo de audio si existe y subirlo a Cloudinary
        audio_url = None
        audio_data = request.FILES.get('audio')
        if audio_data:
            audio_url = self.subir_audio_a_cloudinary(audio_data)

        # Crear una copia mutable del QueryDict
        solicitud_data = request.POST.copy()
        solicitud_data['audio'] = audio_url

        solicitud_serializer = SolicitudAsistenciaSerializer(data=solicitud_data)
        if solicitud_serializer.is_valid():
            with transaction.atomic():
                solicitud = solicitud_serializer.save()

                # Procesar las imágenes
                imagenes_data = request.FILES.getlist('imagenes')
                for img_data in imagenes_data:
                    ImagenSolicitud.objects.create(solicitud=solicitud, foto=img_data)

                self.enviar_notificacion_a_talleres(solicitud)
                return Response(solicitud_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(solicitud_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def enviar_notificacion_a_talleres(self, solicitud):
        User = get_user_model()
        talleres = User.objects.filter(user_type=3)  # Suponiendo que 3 es el tipo para talleres
        print(talleres)
        # Crear un mensaje para cada dispositivo
        devices = FCMDevice.objects.filter(user__in=talleres, active=True)
        # Obtenemos el ID del cliente desde el objeto solicitud
        id_cliente = solicitud.cliente.id
        for device in devices:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Nueva solicitud de asistencia Tecnica :O",
                    body=f"Solicitud #{solicitud.id} creada"
                ),
                data={
                    "solicitud_id": str(solicitud.id),
                    "cliente_id": str(id_cliente),  # Añadimos el ID del cliente aquí
                },
                token=device.registration_id  # Importante para enviar a un dispositivo específico
            )

            # Enviar la notificación
            try:
                response = messaging.send(message)  # Se usa la app predeterminada
                print('Successfully sent message:', response)
            except Exception as e:
                print('Error sending message:', e)

class ImagenSolicitudViewSet(viewsets.ModelViewSet):
    queryset = ImagenSolicitud.objects.all()
    serializer_class = ImagenSolicitudSerializer


class PostulacionViewSet(viewsets.ModelViewSet):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario_id')
        # Eliminar el usuario_id de request.data si está presente para evitar errores de deserialización
        if 'usuario_id' in request.data:
            request.data.pop('usuario_id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        # Aquí puedes enviar la notificación al usuario_id
        # Supongamos que tienes una función send_notification(usuario_id)
        if usuario_id:
            self.send_notification(usuario_id, serializer.instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_notification(self, usuario_id, postulacion):
        User = get_user_model()
        print(postulacion.taller.id)
        try:
            # Busca el dispositivo asociado con el usuario
            device = FCMDevice.objects.get(user_id=usuario_id, active=True)

            # Crea el mensaje basado en la información de la solicitud
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Nueva postulación recibida",
                    body=f"Postulación recibida para la solicitud #{postulacion.id}"
                ),
                data={
                    "postulacion_id": str(postulacion.id),
                    "taller_id": str(postulacion.taller.id),
                },
                token=device.registration_id
            )

            # Enviar la notificación
            response = messaging.send(message)
            print('Successfully sent message:', response)
        except FCMDevice.DoesNotExist:
            print(f"No device found for user {usuario_id}")
        except Exception as e:
            print('Error sending message:', e)