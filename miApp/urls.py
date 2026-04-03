from django.urls import path
from miApp.views import (
    Home, ListaGrupos, GrupoAlta, GrupoEditar, GrupoEliminar, 
    ListaVehiculos, VehiculoAlta, VehiculoEditar, VehiculoEliminar,
    ListaContactos, ContactoAlta, ContactoEditar, ContactoEliminar,
    ListaUsuarios, UsuarioAlta, UsuarioEditar, UsuarioEliminar,
    ListaViajes, ViajeAlta, ViajeEditar, ViajeEliminar)

urlpatterns = [
    path('', Home.as_view(), name='home'),
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
    path('usuarios/alta/', UsuarioAlta.as_view(), name='usuarioAlta'),
    path('usuarios/editar/<int:usuario_id>/', UsuarioEditar.as_view(), name='usuarioEditar'),
    path('usuarios/eliminar/<int:usuario_id>/', UsuarioEliminar.as_view(), name='usuarioEliminar'),
    path('viajes/', ListaViajes.as_view(), name='viajes'),
    path('viajes/alta/', ViajeAlta.as_view(), name='viajeAlta'),
    path('viajes/editar/<int:viaje_id>/', ViajeEditar.as_view(), name='viajeEditar'),
    path('viajes/eliminar/<int:viaje_id>/', ViajeEliminar.as_view(), name='viajeEliminar'),
]
