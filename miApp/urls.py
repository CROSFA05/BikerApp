from django.urls import path, include
from rest_framework.routers import DefaultRouter
from miApp.views import (
    Home, Register, ListaGrupos, GrupoAlta, GrupoEditar, GrupoEliminar, 
    ListaVehiculos, VehiculoAlta, VehiculoEditar, VehiculoEliminar,
    ListaContactos, ContactoAlta, ContactoEditar, ContactoEliminar,
    ListaUsuarios, UsuarioDetalle, UsuarioAlta, UsuarioEditar, UsuarioEliminar,
    ListaViajes, ViajeAlta, ViajeEditar, ViajeEliminar,
    ChatGrupo)
from miApp.api_views import (
    LoginView, LogoutView, RegisterView, UserProfileView,
    UsuarioViewSet, GrupoBikerViewSet, VehiculoViewSet,
    ContactoEmergenciaViewSet, ViajeViewSet, UsuarioVehiculoViewSet)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'grupos-biker', GrupoBikerViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'contactos-emergencia', ContactoEmergenciaViewSet)
router.register(r'viajes', ViajeViewSet)
router.register(r'usuarios-vehiculos', UsuarioVehiculoViewSet)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
    path('grupos/', ListaGrupos.as_view(), name='grupos'),
    path('grupos/alta/', GrupoAlta.as_view(), name='grupoAlta'),
    path('grupos/editar/<int:grupo_id>/', GrupoEditar.as_view(), name='grupoEditar'),
    path('grupos/eliminar/<int:grupo_id>/', GrupoEliminar.as_view(), name='grupoEliminar'),
    path('vehiculos/', ListaVehiculos.as_view(), name='vehiculos'),
    path('vehiculos/alta/', VehiculoAlta.as_view(), name='vehiculoAlta'),
    path('vehiculos/editar/<int:vehiculo_id>/', VehiculoEditar.as_view(), name='vehiculoEditar'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', VehiculoEliminar.as_view(), name='vehiculoEliminar'),
    path('contactos/', ListaContactos.as_view(), name='contactos'),
    path('contactos/alta/', ContactoAlta.as_view(), name='contactoAlta'),
    path('contactos/editar/<int:contacto_id>/', ContactoEditar.as_view(), name='contactoEditar'),
    path('contactos/eliminar/<int:contacto_id>/', ContactoEliminar.as_view(), name='contactoEliminar'),
    path('usuarios/', ListaUsuarios.as_view(), name='usuarios'),
    path('usuarios/detalle/<int:usuario_id>/', UsuarioDetalle.as_view(), name='usuarioDetalle'),
    path('usuarios/alta/', UsuarioAlta.as_view(), name='usuarioAlta'),
    path('usuarios/editar/<int:usuario_id>/', UsuarioEditar.as_view(), name='usuarioEditar'),
    path('usuarios/eliminar/<int:usuario_id>/', UsuarioEliminar.as_view(), name='usuarioEliminar'),
    path('viajes/', ListaViajes.as_view(), name='viajes'),
    path('viajes/alta/', ViajeAlta.as_view(), name='viajeAlta'),
    path('viajes/editar/<int:viaje_id>/', ViajeEditar.as_view(), name='viajeEditar'),
    path('viajes/eliminar/<int:viaje_id>/', ViajeEliminar.as_view(), name='viajeEliminar'),
    path('chat/', ChatGrupo.as_view(), name='chat_grupo'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/perfil/', UserProfileView.as_view(), name='api_perfil'),
    path('api/', include(router.urls)),
]
