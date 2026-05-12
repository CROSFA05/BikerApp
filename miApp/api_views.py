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
from .permissions import IsStaffOrReadOnly, IsOwnerOrStaff, SameGroupOrStaff, IsLeaderOrStaff, SameGroupViewOwnerEdit


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
    permission_classes = [SameGroupOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            usuarios = Usuario.objects.all()
        elif user.grupo_biker:
            usuarios = Usuario.objects.filter(grupo_biker=user.grupo_biker)
        else:
            usuarios = Usuario.objects.filter(id=user.id)
        return sorted(usuarios, key=lambda u: u.id != user.id)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [SameGroupOrStaff()]

    def check_object_permissions(self, request, obj):
        if self.action in ['update', 'partial_update']:
            if not (request.user.is_staff or obj == request.user):
                self.permission_denied(request)
        super().check_object_permissions(request, obj)


class GrupoBikerViewSet(viewsets.ModelViewSet):
    queryset = GrupoBiker.objects.all()
    serializer_class = GrupoBikerSerializer
    permission_classes = [IsLeaderOrStaff]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]
        return [IsLeaderOrStaff()]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.all()
    serializer_class = ContactoEmergenciaSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ContactoEmergencia.objects.all()
        return ContactoEmergencia.objects.filter(usuario=user)


class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
    permission_classes = [SameGroupViewOwnerEdit]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Viaje.objects.all()
        if user.grupo_biker:
            return Viaje.objects.filter(usuario__grupo_biker=user.grupo_biker)
        return Viaje.objects.filter(usuario=user)


class UsuarioVehiculoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioVehiculo.objects.all()
    serializer_class = UsuarioVehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
