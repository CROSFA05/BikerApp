from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import Usuario, GrupoBiker, Vehiculo, ContactoEmergencia, Viaje, UsuarioVehiculo


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales inválidas')
        if not user.is_active:
            raise serializers.ValidationError('Usuario inactivo')
        data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'password', 'password2',
                  'sexo', 'fecha_nacimiento', 'telefono']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['username'] = validated_data['email']
        return Usuario.objects.create(**validated_data)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'first_name', 'last_name', 'rol', 'sexo',
                  'fecha_nacimiento', 'tipo_de_sangre', 'enfermedades',
                  'alergias', 'nss', 'poliza_seguro', 'aseguradora',
                  'telefono', 'grupo_biker', 'activo', 'is_staff', 'is_active']
        read_only_fields = ['id', 'is_staff', 'is_active']


class GrupoBikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoBiker
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class ContactoEmergenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactoEmergencia
        fields = '__all__'


class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'


class UsuarioVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioVehiculo
        fields = '__all__'
