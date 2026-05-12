from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import GrupoBiker, Vehiculo, ContactoEmergencia, Usuario, Viaje, UsuarioVehiculo
from .forms import GrupoBikerForm, VehiculoForm, ContactoEmergenciaForm, UsuarioForm, UsuarioChangeForm, ViajeForm

class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            grupo = user.grupo_biker
            if user.is_staff:
                viajes_count = Viaje.objects.count()
                contactos_count = ContactoEmergencia.objects.count()
                vehiculos_count = UsuarioVehiculo.objects.count()
            elif grupo:
                viajes_count = Viaje.objects.filter(usuario__grupo_biker=grupo).count()
                contactos_count = ContactoEmergencia.objects.filter(usuario__grupo_biker=grupo).count()
                vehiculos_count = UsuarioVehiculo.objects.filter(usuario__grupo_biker=grupo).count()
            else:
                viajes_count = Viaje.objects.filter(usuario=user).count()
                contactos_count = ContactoEmergencia.objects.filter(usuario=user).count()
                vehiculos_count = UsuarioVehiculo.objects.filter(usuario=user).count()
            cdx = {
                'titulo': 'Inicio - Biker App',
                'info_usuario': user,
                'grupo': grupo,
                'stats': {
                    'viajes': viajes_count,
                    'contactos': contactos_count,
                    'vehiculos': vehiculos_count,
                },
            }
            return render(request, 'home.html', cdx)
        else:
            cdx = {'titulo': 'Bienvenido - Biker App'}
            return render(request, 'landing.html', cdx)

class Register(View):
    def get(self, request):
        form = UsuarioForm()
        cdx = {'titulo': 'Registro - Biker App', 'form': form}
        return render(request, 'registration/register.html', cdx)
    
    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('home')
        cdx = {'titulo': 'Registro - Biker App', 'form': form}
        return render(request, 'registration/register.html', cdx)

class ListaGrupos(LoginRequiredMixin, View):
    def get(self, request):
        grupos = GrupoBiker.objects.all()
        cdx = {'grupos': grupos}
        return render(request, 'GrupoBiker/grupoBiker.html', cdx)

class GrupoAlta(LoginRequiredMixin, View):
    def get(self, request):
        form = GrupoBikerForm()
        cdx = {'titulo': 'Alta de Grupo', 'form': form, 'modo': 'crear'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)
        
    def post(self, request):
        form = GrupoBikerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo creado exitosamente')
            return redirect('grupos')
        cdx = {'titulo': 'Alta de Grupo', 'form': form, 'modo': 'crear'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)

class GrupoEditar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        grupo = get_object_or_404(GrupoBiker, pk=kwargs.get('grupo_id'))
        if not (request.user.is_staff or grupo.lider == request.user):
            return HttpResponseForbidden('No tienes permiso para editar este grupo')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        form = GrupoBikerForm(instance=grupo)
        cdx = {'titulo': 'Editar Grupo', 'form': form, 'grupo': grupo, 'modo': 'editar'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)
    
    def post(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        form = GrupoBikerForm(request.POST, request.FILES, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado exitosamente')
            return redirect('grupos')
        cdx = {'titulo': 'Editar Grupo', 'form': form, 'grupo': grupo, 'modo': 'editar'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)

class GrupoEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden eliminar grupos')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        grupo.delete()
        messages.success(request, 'Grupo eliminado exitosamente')
        return redirect('grupos')

class ListaVehiculos(LoginRequiredMixin, View):
    def get(self, request):
        vehiculos = Vehiculo.objects.all()
        cdx = {'vehiculos': vehiculos}
        return render(request, 'Vehiculo/vehiculo.html', cdx)

class VehiculoAlta(LoginRequiredMixin, View):
    def get(self, request):
        form = VehiculoForm(initial={'usuarios': [request.user]})
        cdx = {'titulo': 'Alta de Vehiculo', 'form': form, 'modo': 'crear'}
        return render(request, 'Vehiculo/vehiculoCRUD.html', cdx)
    
    def post(self, request):
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehiculo creado exitosamente')
            return redirect('vehiculos')
        cdx = {'titulo': 'Alta de Vehiculo', 'form': form, 'modo': 'crear'}
        return render(request, 'Vehiculo/vehiculoCRUD.html', cdx)

class VehiculoEditar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        vehiculo = get_object_or_404(Vehiculo, pk=kwargs.get('vehiculo_id'))
        if not (request.user.is_staff or vehiculo.usuarios.filter(id=request.user.id).exists()):
            return HttpResponseForbidden('No tienes permiso para editar este vehículo')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, vehiculo_id):
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        form = VehiculoForm(instance=vehiculo)
        cdx = {'titulo': 'Editar Vehiculo', 'form': form, 'vehiculo': vehiculo, 'modo': 'editar'}
        return render(request, 'Vehiculo/vehiculoCRUD.html', cdx)
    
    def post(self, request, vehiculo_id):
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehiculo actualizado exitosamente')
            return redirect('vehiculos')
        cdx = {'titulo': 'Editar Vehiculo', 'form': form, 'vehiculo': vehiculo, 'modo': 'editar'}
        return render(request, 'Vehiculo/vehiculoCRUD.html', cdx)

class VehiculoEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden eliminar vehículos')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, vehiculo_id):
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        vehiculo.delete()
        messages.success(request, 'Vehiculo eliminado exitosamente')
        return redirect('vehiculos')

class ListaContactos(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            contactos = ContactoEmergencia.objects.select_related('usuario').all()
        else:
            contactos = ContactoEmergencia.objects.select_related('usuario').filter(usuario=request.user)
        cdx = {'contactos': contactos}
        return render(request, 'Contactos/contactoEmergencia.html', cdx)

class ContactoAlta(LoginRequiredMixin, View):
    def get(self, request):
        form = ContactoEmergenciaForm()
        cdx = {'titulo': 'Alta de Contacto de Emergencia', 'form': form, 'modo': 'crear'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)
    
    def post(self, request):
        form = ContactoEmergenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto creado exitosamente')
            return redirect('contactos')
        cdx = {'titulo': 'Alta de Contacto de Emergencia', 'form': form, 'modo': 'crear'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)

class ContactoEditar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        contacto = get_object_or_404(ContactoEmergencia, pk=kwargs.get('contacto_id'))
        if not (request.user.is_staff or contacto.usuario == request.user):
            return HttpResponseForbidden('No tienes permiso para editar este contacto')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, contacto_id):
        contacto = get_object_or_404(ContactoEmergencia, pk=contacto_id)
        form = ContactoEmergenciaForm(instance=contacto)
        cdx = {'titulo': 'Editar Contacto de Emergencia', 'form': form, 'contacto': contacto, 'modo': 'editar'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)
    
    def post(self, request, contacto_id):
        contacto = get_object_or_404(ContactoEmergencia, pk=contacto_id)
        form = ContactoEmergenciaForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto actualizado exitosamente')
            return redirect('contactos')
        cdx = {'titulo': 'Editar Contacto de Emergencia', 'form': form, 'contacto': contacto, 'modo': 'editar'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)

class ContactoEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        contacto = get_object_or_404(ContactoEmergencia, pk=kwargs.get('contacto_id'))
        if not (request.user.is_staff or contacto.usuario == request.user):
            return HttpResponseForbidden('No tienes permiso para eliminar este contacto')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, contacto_id):
        contacto = get_object_or_404(ContactoEmergencia, pk=contacto_id)
        contacto.delete()
        messages.success(request, 'Contacto eliminado exitosamente')
        return redirect('contactos')

class ListaUsuarios(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            usuarios = Usuario.objects.select_related('grupo_biker').all()
        elif request.user.grupo_biker:
            usuarios = Usuario.objects.select_related('grupo_biker').filter(grupo_biker=request.user.grupo_biker)
        else:
            usuarios = Usuario.objects.filter(id=request.user.id)
        usuarios = sorted(usuarios, key=lambda u: u.id != request.user.id)
        cdx = {'usuarios': usuarios}
        return render(request, 'Usuario/usuario.html', cdx)

class UsuarioAlta(LoginRequiredMixin, View):
    def get(self, request):
        form = UsuarioForm()
        cdx = {'titulo': 'Alta de Usuario', 'form': form, 'modo': 'crear'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)
    
    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('usuarios')
        cdx = {'titulo': 'Alta de Usuario', 'form': form, 'modo': 'crear'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)

class UsuarioEditar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=kwargs.get('usuario_id'))
        if not (request.user.is_staff or request.user == usuario):
            return HttpResponseForbidden('No tienes permiso para editar este perfil')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        form = UsuarioChangeForm(instance=usuario)
        cdx = {'titulo': 'Editar Usuario', 'form': form, 'usuario': usuario, 'modo': 'editar'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)
    
    def post(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente')
            return redirect('usuarios')
        cdx = {'titulo': 'Editar Usuario', 'form': form, 'usuario': usuario, 'modo': 'editar'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)

class UsuarioEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden eliminar usuarios')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente')
        return redirect('usuarios')

class ListaViajes(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            viajes = Viaje.objects.select_related('usuario').all()
        elif request.user.grupo_biker:
            viajes = Viaje.objects.select_related('usuario').filter(usuario__grupo_biker=request.user.grupo_biker)
        else:
            viajes = Viaje.objects.filter(usuario=request.user)
        cdx = {'viajes': viajes}
        return render(request, 'Viaje/viaje.html', cdx)

class ViajeAlta(LoginRequiredMixin, View):
    def get(self, request):
        form = ViajeForm()
        cdx = {'titulo': 'Alta de Viaje', 'form': form, 'modo': 'crear'}
        return render(request, 'Viaje/viajeCRUD.html', cdx)
    
    def post(self, request):
        form = ViajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje creado exitosamente')
            return redirect('viajes')
        cdx = {'titulo': 'Alta de Viaje', 'form': form, 'modo': 'crear'}
        return render(request, 'Viaje/viajeCRUD.html', cdx)

class ViajeEditar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        viaje = get_object_or_404(Viaje, pk=kwargs.get('viaje_id'))
        if not (request.user.is_staff or viaje.usuario == request.user):
            return HttpResponseForbidden('No tienes permiso para editar este viaje')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, viaje_id):
        viaje = get_object_or_404(Viaje, pk=viaje_id)
        form = ViajeForm(instance=viaje)
        cdx = {'titulo': 'Editar Viaje', 'form': form, 'viaje': viaje, 'modo': 'editar'}
        return render(request, 'Viaje/viajeCRUD.html', cdx)
    
    def post(self, request, viaje_id):
        viaje = get_object_or_404(Viaje, pk=viaje_id)
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje actualizado exitosamente')
            return redirect('viajes')
        cdx = {'titulo': 'Editar Viaje', 'form': form, 'viaje': viaje, 'modo': 'editar'}
        return render(request, 'Viaje/viajeCRUD.html', cdx)

class ViajeEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        viaje = get_object_or_404(Viaje, pk=kwargs.get('viaje_id'))
        if not (request.user.is_staff or viaje.usuario == request.user):
            return HttpResponseForbidden('No tienes permiso para eliminar este viaje')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, viaje_id):
        viaje = get_object_or_404(Viaje, pk=viaje_id)
        viaje.delete()
        messages.success(request, 'Viaje eliminado exitosamente')
        return redirect('viajes')
