from django.forms import ModelForm, Select, DateInput, ModelMultipleChoiceField, CheckboxSelectMultiple, FileInput, TextInput, Textarea
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
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            self.fields['usuario'].queryset = Usuario.objects.filter(id=user.id)
            self.fields['usuario'].initial = user
            self.fields['usuario'].empty_label = None
        else:
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
                  'aseguradora', 'telefono', 'grupo_biker', 'activo', 'imagen']
        widgets = {
            'grupo_biker': Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'sexo': Select(attrs={'class': 'form-select'}),
            'tipo_de_sangre': Select(attrs={'class': 'form-select'}),
            'rol': Select(attrs={'class': 'form-select'}),
            'imagen': FileInput(attrs={'class': 'form-input'}),
            'email': TextInput(attrs={'class': 'form-input', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre(s)'}),
            'last_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Apellido(s)'}),
            'telefono': TextInput(attrs={'class': 'form-input', 'maxlength': '10', 'placeholder': '10 dígitos'}),
            'enfermedades': Textarea(attrs={'class': 'form-input', 'rows': '2', 'placeholder': 'Describe cualquier enfermedad relevante...'}),
            'alergias': Textarea(attrs={'class': 'form-input', 'rows': '2', 'placeholder': 'Describe cualquier alergia importante...'}),
            'nss': TextInput(attrs={'class': 'form-input', 'maxlength': '11', 'placeholder': '11 dígitos'}),
            'poliza_seguro': TextInput(attrs={'class': 'form-input', 'maxlength': '50', 'placeholder': 'Número de póliza'}),
            'aseguradora': TextInput(attrs={'class': 'form-input', 'maxlength': '50', 'placeholder': 'Nombre de la aseguradora'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo_biker'].queryset = GrupoBiker.objects.filter(activo=True)
        self.fields['grupo_biker'].required = False
        self.fields['rol'].required = False
        self.fields['sexo'].required = False
        self.fields['tipo_de_sangre'].required = False
        self.fields['fecha_nacimiento'].required = False

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
                  'aseguradora', 'telefono', 'grupo_biker', 'activo', 'imagen', 'is_active', 'is_staff']
        widgets = {
            'grupo_biker': Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'sexo': Select(attrs={'class': 'form-select'}),
            'tipo_de_sangre': Select(attrs={'class': 'form-select'}),
            'rol': Select(attrs={'class': 'form-select'}),
            'imagen': FileInput(attrs={'class': 'form-input'}),
            'email': TextInput(attrs={'class': 'form-input', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre(s)'}),
            'last_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Apellido(s)'}),
            'telefono': TextInput(attrs={'class': 'form-input', 'maxlength': '10', 'placeholder': '10 dígitos'}),
            'enfermedades': Textarea(attrs={'class': 'form-input', 'rows': '2', 'placeholder': 'Describe cualquier enfermedad relevante...'}),
            'alergias': Textarea(attrs={'class': 'form-input', 'rows': '2', 'placeholder': 'Describe cualquier alergia importante...'}),
            'nss': TextInput(attrs={'class': 'form-input', 'maxlength': '11', 'placeholder': '11 dígitos'}),
            'poliza_seguro': TextInput(attrs={'class': 'form-input', 'maxlength': '50', 'placeholder': 'Número de póliza'}),
            'aseguradora': TextInput(attrs={'class': 'form-input', 'maxlength': '50', 'placeholder': 'Nombre de la aseguradora'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo_biker'].queryset = GrupoBiker.objects.filter(activo=True)
        self.fields['grupo_biker'].required = False
        self.fields['rol'].required = False
        self.fields['sexo'].required = False
        self.fields['tipo_de_sangre'].required = False
        self.fields['fecha_nacimiento'].required = False
        if self.instance.pk:
            self.fields['vehiculos'].initial = self.instance.vehiculos.all()

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
