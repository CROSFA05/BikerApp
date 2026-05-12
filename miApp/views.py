from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import GrupoBiker, Vehiculo, ContactoEmergencia, Usuario, Viaje, UsuarioVehiculo, MensajeGrupo
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
                'titulo': 'Usuario - Biker App',
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
        form = UsuarioForm(request.POST, request.FILES)
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden crear grupos')
        return super().dispatch(request, *args, **kwargs)

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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden crear vehículos')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = VehiculoForm()
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
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden editar vehículos')
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
        form = ContactoEmergenciaForm(user=request.user)
        cdx = {'titulo': 'Alta de Contacto de Emergencia', 'form': form, 'modo': 'crear'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)
    
    def post(self, request):
        form = ContactoEmergenciaForm(request.POST, user=request.user)
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
        form = ContactoEmergenciaForm(instance=contacto, user=request.user)
        cdx = {'titulo': 'Editar Contacto de Emergencia', 'form': form, 'contacto': contacto, 'modo': 'editar'}
        return render(request, 'Contactos/contactoCRUD.html', cdx)
    
    def post(self, request, contacto_id):
        contacto = get_object_or_404(ContactoEmergencia, pk=contacto_id)
        form = ContactoEmergenciaForm(request.POST, instance=contacto, user=request.user)
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
            usuarios = Usuario.objects.select_related('grupo_biker').exclude(id=request.user.id).all()
        elif request.user.grupo_biker:
            usuarios = Usuario.objects.select_related('grupo_biker').filter(grupo_biker=request.user.grupo_biker).exclude(id=request.user.id)
        else:
            usuarios = Usuario.objects.none()
        cdx = {'usuarios': usuarios}
        return render(request, 'Usuario/usuario.html', cdx)

class UsuarioDetalle(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=kwargs.get('usuario_id'))
        if not (request.user.is_staff or request.user == usuario or (
            request.user.grupo_biker and usuario.grupo_biker == request.user.grupo_biker
        )):
            return HttpResponseForbidden('No tienes permiso para ver este perfil')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        grupo = usuario.grupo_biker
        if request.user.is_staff:
            viajes_count = Viaje.objects.filter(usuario=usuario).count()
            contactos_count = ContactoEmergencia.objects.filter(usuario=usuario).count()
            vehiculos_count = UsuarioVehiculo.objects.filter(usuario=usuario).count()
        elif grupo:
            viajes_count = Viaje.objects.filter(usuario=usuario).count()
            contactos_count = ContactoEmergencia.objects.filter(usuario=usuario).count()
            vehiculos_count = UsuarioVehiculo.objects.filter(usuario=usuario).count()
        else:
            viajes_count = Viaje.objects.filter(usuario=usuario).count()
            contactos_count = ContactoEmergencia.objects.filter(usuario=usuario).count()
            vehiculos_count = UsuarioVehiculo.objects.filter(usuario=usuario).count()
        cdx = {
            'titulo': f'{usuario.first_name} {usuario.last_name} - Biker App',
            'info_usuario': usuario,
            'grupo': grupo,
            'stats': {
                'viajes': viajes_count,
                'contactos': contactos_count,
                'vehiculos': vehiculos_count,
            },
            'es_perfil_propio': request.user == usuario,
        }
        return render(request, 'Usuario/usuarioDetalle.html', cdx)

class UsuarioAlta(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Solo administradores pueden crear usuarios')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UsuarioForm()
        vehiculos_list = Vehiculo.objects.all().values('id', 'marca', 'modelo', 'matricula', 'año')
        cdx = {'titulo': 'Alta de Usuario', 'form': form, 'modo': 'crear', 'vehiculos_list': vehiculos_list}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)
    
    def post(self, request):
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UsuarioVehiculo.objects.filter(usuario=user).delete()
            for v in form.cleaned_data.get('vehiculos', []):
                UsuarioVehiculo.objects.create(usuario=user, vehiculo=v)
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
        vehiculos_list = Vehiculo.objects.all().values('id', 'marca', 'modelo', 'matricula', 'año')
        cdx = {'titulo': 'Editar Usuario', 'form': form, 'usuario': usuario, 'modo': 'editar', 'vehiculos_list': vehiculos_list}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)
    
    def post(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        form = UsuarioChangeForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            UsuarioVehiculo.objects.filter(usuario=usuario).delete()
            for v in form.cleaned_data.get('vehiculos', []):
                UsuarioVehiculo.objects.create(usuario=usuario, vehiculo=v)
            messages.success(request, 'Usuario actualizado exitosamente')
            return redirect('usuarios')
        cdx = {'titulo': 'Editar Usuario', 'form': form, 'usuario': usuario, 'modo': 'editar'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)

class UsuarioEliminar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=kwargs.get('usuario_id'))
        if not (request.user.is_staff or request.user == usuario):
            return HttpResponseForbidden('No tienes permiso para eliminar este usuario')
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


class ChatGrupo(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.grupo_biker and not request.user.is_staff:
            return HttpResponseForbidden('Debes pertenecer a un grupo para usar el chat')
        return super().dispatch(request, *args, **kwargs)

    def get_grupo(self, request):
        if request.user.is_staff and 'grupo_id' in self.kwargs:
            return get_object_or_404(GrupoBiker, pk=self.kwargs['grupo_id'])
        return request.user.grupo_biker

    def get(self, request, **kwargs):
        grupo = self.get_grupo(request)
        if not grupo:
            return HttpResponseForbidden('No hay grupo asignado')
        mensajes = MensajeGrupo.obtener_historial(grupo)
        cdx = {
            'grupo': grupo,
            'mensajes': mensajes,
            'total_mensajes': MensajeGrupo.objects.filter(grupo=grupo).count(),
            'limite': MensajeGrupo.LIMITE(),
        }
        return render(request, 'Chat/chatGrupo.html', cdx)

    def post(self, request, **kwargs):
        grupo = self.get_grupo(request)
        if not grupo:
            return HttpResponseForbidden('No hay grupo asignado')
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            MensajeGrupo.enviar(grupo, request.user, contenido)
        else:
            messages.error(request, 'El mensaje no puede estar vacío')
        return redirect('chat_grupo')
