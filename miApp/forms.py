from django.forms import ModelForm, Select
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from miApp.models import GrupoBiker, Vehiculo, ContactoEmergencia, Usuario, Viaje

class GrupoBikerForm(ModelForm):
    class Meta:
        model = GrupoBiker
        fields = ['nombre', 'descripcion', 'activo']

class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'año', 'color', 'matricula', 'tipo_vehiculo']

class ContactoEmergenciaForm(ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['usuario', 'nombre', 'telefono', 'relacion']
        widgets = {
            'usuario': Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuarios_con_contacto = ContactoEmergencia.objects.values_list('usuario_id', flat=True)
        self.fields['usuario'].queryset = Usuario.objects.filter(is_active=True).exclude(id__in=usuarios_con_contacto)

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'sexo', 'fecha_nacimiento', 
                  'tipo_de_sangre', 'enfermedades', 'alergias', 'nss', 'poliza_seguro',
                  'aseguradora', 'telefono', 'grupo_biker', 'activo']
        widgets = {
            'grupo_biker': Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': Select(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo_biker'].queryset = GrupoBiker.objects.filter(activo=True)
        self.fields['grupo_biker'].required = False

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'sexo', 'fecha_nacimiento', 
                  'tipo_de_sangre', 'enfermedades', 'alergias', 'nss', 'poliza_seguro',
                  'aseguradora', 'telefono', 'grupo_biker', 'activo', 'is_active', 'is_staff']
        widgets = {
            'grupo_biker': Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': Select(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo_biker'].queryset = GrupoBiker.objects.filter(activo=True)
        self.fields['grupo_biker'].required = False

class ViajeForm(ModelForm):
    class Meta:
        model = Viaje
        fields = ['usuario', 'estado', 'lugar_de_inicio', 'lugar_de_fin', 
                  'distancia_estimada', 'duracion_estimada']
        widgets = {
            'usuario': Select(attrs={'class': 'form-select'}),
            'estado': Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(is_active=True)
        self.fields['lugar_de_fin'].required = False
        self.fields['distancia_estimada'].required = False
        self.fields['duracion_estimada'].required = False
