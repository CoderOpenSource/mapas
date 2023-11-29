from fcm_django.models import FCMDevice
from rest_framework import viewsets
from .models import Cliente, Taller, Tecnico, CustomUser
from .serializers import ClienteSerializer, TallerSerializer, TecnicoSerializer, CustomUserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
        fcm_token = serializer.validated_data.get('fcm_token')
        token_message = ''

        # Verificar si el token ya está asociado con el usuario
        print(fcm_token)
        if fcm_token:
            # Primero, intenta obtener un dispositivo FCM existente con el mismo token
            existing_device = FCMDevice.objects.filter(registration_id=fcm_token).first()

            # Si el dispositivo ya existe y está asociado con otro usuario, actualiza el usuario
            if existing_device and existing_device.user != user:
                existing_device.user = user
                existing_device.save()
                token_message = 'FCM token updated successfully.'
            # Si no existe un dispositivo con ese token, crea uno nuevo
            elif not existing_device:
                FCMDevice.objects.create(
                    user=user,
                    registration_id=fcm_token,
                    type='android'
                )
                token_message = 'FCM token registered successfully.'

            else:
                token_message = 'FCM token already registered with this user.'
        # Create token
        refresh = RefreshToken.for_user(user)
        print(token_message)
        # Get the photo URL if exists
        foto_url = user.foto.url if user.foto else None

        # Get the text representation of the user type
        user_type = dict(User.USER_TYPE_CHOICES).get(user.user_type, None)

        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'foto': foto_url,
            'user_type': user_type  # Here we return the user type as text
        }

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_data': user_data,
            'token_message': token_message,
            'token': fcm_token    # Agregar mensaje del token aquí
        })


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
