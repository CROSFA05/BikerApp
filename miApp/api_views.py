from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import Usuario, GrupoBiker, Vehiculo, ContactoEmergencia, Viaje, UsuarioVehiculo
from .serializers import (
    LoginSerializer, RegisterSerializer, UsuarioSerializer,
    GrupoBikerSerializer, VehiculoSerializer, ContactoEmergenciaSerializer,
    ViajeSerializer, UsuarioVehiculoSerializer
)
from .permissions import IsStaffOrReadOnly, IsOwnerOrStaff


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'mensaje': 'Sesión cerrada exitosamente'})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer

    def get_object(self):
        return self.request.user


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class GrupoBikerViewSet(viewsets.ModelViewSet):
    queryset = GrupoBiker.objects.all()
    serializer_class = GrupoBikerSerializer
    permission_classes = [IsStaffOrReadOnly]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.all()
    serializer_class = ContactoEmergenciaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioVehiculoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioVehiculo.objects.all()
    serializer_class = UsuarioVehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
