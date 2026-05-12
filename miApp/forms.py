from django.forms import ModelForm, Select, DateInput, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from miApp.models import GrupoBiker, Vehiculo, ContactoEmergencia, Usuario, Viaje, UsuarioVehiculo

class GrupoBikerForm(ModelForm):
    class Meta:
        model = GrupoBiker
        fields = ['nombre', 'descripcion', 'activo', 'lider', 'imagen']

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
    vehiculos = ModelMultipleChoiceField(
        queryset=Vehiculo.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Vehículos asignados'
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'rol', 'sexo', 'fecha_nacimiento', 
                  'tipo_de_sangre', 'enfermedades', 'alergias', 'nss', 'poliza_seguro',
                  'aseguradora', 'telefono', 'grupo_biker', 'activo']
        widgets = {
            'grupo_biker': Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'sexo': Select(attrs={'class': 'form-select'}),
            'tipo_de_sangre': Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo_biker'].queryset = GrupoBiker.objects.filter(activo=True)
        self.fields['grupo_biker'].required = False
        for field_name, field in self.fields.items():
            if field_name not in ['grupo_biker', 'fecha_nacimiento', 'sexo', 'tipo_de_sangre', 'vehiculos']:
                field.widget.attrs['class'] = 'form-input'

    def save(self, commit=True):
        user = super().save(commit=True)
        UsuarioVehiculo.objects.filter(usuario=user).delete()
        for v in self.cleaned_data.get('vehiculos', []):
            UsuarioVehiculo.objects.create(usuario=user, vehiculo=v)
        return user

class UsuarioChangeForm(UserChangeForm):
    vehiculos = ModelMultipleChoiceField(
        queryset=Vehiculo.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Vehículos asignados'
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'rol', 'sexo', 'fecha_nacimiento', 
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
        if self.instance.pk:
            self.fields['vehiculos'].initial = self.instance.vehiculos.all()

    def save(self, commit=True):
        user = super().save(commit=True)
        UsuarioVehiculo.objects.filter(usuario=user).delete()
        for v in self.cleaned_data.get('vehiculos', []):
            UsuarioVehiculo.objects.create(usuario=user, vehiculo=v)
        return user

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
