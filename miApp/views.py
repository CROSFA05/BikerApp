from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import GrupoBiker, Vehiculo, ContactoEmergencia, Usuario, Viaje
from .forms import GrupoBikerForm, VehiculoForm, ContactoEmergenciaForm, UsuarioForm, UsuarioChangeForm, ViajeForm

class Home(View):
    def get(self, request):
        cdx = {'titulo': 'Usuario'}
        return render(request, 'User/user.html', cdx)

class ListaGrupos(View):
    def get(self, request):
        grupos = GrupoBiker.objects.all()
        cdx = {'grupos': grupos}
        return render(request, 'GrupoBiker/grupoBiker.html', cdx)

class GrupoAlta(View):
    def get(self, request):
        form = GrupoBikerForm()
        cdx = {'titulo': 'Alta de Grupo', 'form': form, 'modo': 'crear'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)
        
    def post(self, request):
        form = GrupoBikerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo creado exitosamente')
            return redirect('grupos')
        cdx = {'titulo': 'Alta de Grupo', 'form': form, 'modo': 'crear'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)

class GrupoEditar(View):
    def get(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        form = GrupoBikerForm(instance=grupo)
        cdx = {'titulo': 'Editar Grupo', 'form': form, 'grupo': grupo, 'modo': 'editar'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)
    
    def post(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        form = GrupoBikerForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado exitosamente')
            return redirect('grupos')
        cdx = {'titulo': 'Editar Grupo', 'form': form, 'grupo': grupo, 'modo': 'editar'}
        return render(request, 'GrupoBiker/grupoCRUD.html', cdx)

class GrupoEliminar(View):
    def post(self, request, grupo_id):
        grupo = get_object_or_404(GrupoBiker, pk=grupo_id)
        grupo.delete()
        messages.success(request, 'Grupo eliminado exitosamente')
        return redirect('grupos')

class ListaVehiculos(View):
    def get(self, request):
        vehiculos = Vehiculo.objects.all()
        cdx = {'vehiculos': vehiculos}
        return render(request, 'Vehiculo/vehiculo.html', cdx)

class VehiculoAlta(View):
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

class VehiculoEditar(View):
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

class VehiculoEliminar(View):
    def post(self, request, vehiculo_id):
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        vehiculo.delete()
        messages.success(request, 'Vehiculo eliminado exitosamente')
        return redirect('vehiculos')

class ListaContactos(View):
    def get(self, request):
        contactos = ContactoEmergencia.objects.select_related('usuario').all()
        cdx = {'contactos': contactos}
        return render(request, 'Contactos/contactoEmergencia.html', cdx)

class ContactoAlta(View):
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

class ContactoEditar(View):
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

class ContactoEliminar(View):
    def post(self, request, contacto_id):
        contacto = get_object_or_404(ContactoEmergencia, pk=contacto_id)
        contacto.delete()
        messages.success(request, 'Contacto eliminado exitosamente')
        return redirect('contactos')

class ListaUsuarios(View):
    def get(self, request):
        usuarios = Usuario.objects.select_related('grupo_biker').all()
        cdx = {'usuarios': usuarios}
        return render(request, 'Usuario/usuario.html', cdx)

class UsuarioAlta(View):
    def get(self, request):
        form = UsuarioForm()
        cdx = {'titulo': 'Alta de Usuario', 'form': form, 'modo': 'crear'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)
    
    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            usuario.password = make_password(password)
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('usuarios')
        cdx = {'titulo': 'Alta de Usuario', 'form': form, 'modo': 'crear'}
        return render(request, 'Usuario/usuarioCRUD.html', cdx)

class UsuarioEditar(View):
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

class UsuarioEliminar(View):
    def post(self, request, usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente')
        return redirect('usuarios')

class ListaViajes(View):
    def get(self, request):
        viajes = Viaje.objects.select_related('usuario').all()
        cdx = {'viajes': viajes}
        return render(request, 'Viaje/viaje.html', cdx)

class ViajeAlta(View):
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

class ViajeEditar(View):
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

class ViajeEliminar(View):
    def post(self, request, viaje_id):
        viaje = get_object_or_404(Viaje, pk=viaje_id)
        viaje.delete()
        messages.success(request, 'Viaje eliminado exitosamente')
        return redirect('viajes')
