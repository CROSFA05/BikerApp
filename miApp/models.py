from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class GrupoBiker(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)
    descripcion = models.TextField(max_length = 300)
    activo = models.BooleanField(default = True)

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UsuarioManager()

    class Sexo(models.IntegerChoices):
        PREFIERO_NO_DECIR = 0
        HOMBRE = 1
        MUJER = 2

    class Tipo_De_Sangre(models.IntegerChoices):
        A_POSITIVO = 0
        A_NEGATIVO = 1
        B_POSITIVO = 2
        B_NEGATIVO = 3
        AB_POSITIVO = 4
        AB_NEGATIVO = 5
        O_POSITIVO = 6
        O_NEGATIVO = 7

    sexo = models.IntegerField(choices = Sexo.choices, default=Sexo.PREFIERO_NO_DECIR)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_de_sangre = models.IntegerField(choices = Tipo_De_Sangre.choices, null=True, blank=True)
    enfermedades = models.TextField(max_length = 300, null = True, blank = True, db_index = True)
    alergias = models.TextField(max_length = 300, null = True, blank = True, db_index = True)
    nss = models.CharField(max_length = 11, null = True, blank = True, db_index = True)
    poliza_seguro = models.CharField(max_length = 50, null = True, blank = True, db_index = True)
    aseguradora = models.CharField(max_length = 50, null = True, blank = True)
    telefono = models.CharField(max_length = 10, null = True, blank = True, db_index = True)
    grupo_biker = models.ForeignKey(GrupoBiker, on_delete=models.CASCADE, null = True, blank = True)
    activo = models.BooleanField(default=True)

    vehiculos = models.ManyToManyField('Vehiculo', through='UsuarioVehiculo', related_name='usuarios', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ContactoEmergencia(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='contacto_emergencia')
    nombre = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 10)
    relacion = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.nombre} ({self.relacion}) - {self.usuario}"

class Vehiculo(models.Model):
    class Tipo_Vehiculo(models.IntegerChoices): 
        DEPORTIVA = 0, 'Deportiva'
        TOURING = 1, 'Touring'
        CRUCERO = 2, 'Crucero'
        ENDURO = 3, 'Enduro'
        SCOOTER = 4, 'Scooter'
        NAKED = 5, 'Naked'
        CHOPPER = 6, 'Chopper'
        OTRO = 7, 'Otro'

    marca = models.CharField(max_length = 50)
    modelo = models.CharField(max_length = 50)
    año = models.IntegerField()
    color = models.CharField(max_length = 50)
    matricula = models.CharField(max_length = 15, unique = True)
    tipo_vehiculo = models.IntegerField(choices = Tipo_Vehiculo.choices)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.matricula})"

class UsuarioVehiculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    es_principal = models.BooleanField(default=False)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'vehiculo')

    def __str__(self):
        return f"{self.usuario} - {self.vehiculo}"

class Viaje(models.Model):
    class Estado_De_Viaje(models.IntegerChoices):
        NO_INICIADO = 0, 'No iniciado'
        EN_CURSO = 1, 'En curso'
        FINALIZADO = 2, 'Finalizado'
        PAUSADO = 3, 'Pausado'
        CANCELADO = 4, 'Cancelado'

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null = True, related_name='viajes')
    estado = models.IntegerField(choices = Estado_De_Viaje.choices, default=Estado_De_Viaje.NO_INICIADO)
    fecha_inicio = models.DateTimeField(auto_now_add = True)
    fecha_fin = models.DateTimeField(null = True, blank = True)
    lugar_de_inicio = models.CharField(max_length = 200)
    lugar_de_fin = models.CharField(max_length = 200, null = True, blank = True)
    distancia_estimada = models.FloatField(null = True, blank = True)
    duracion_estimada = models.DurationField(null = True, blank = True)
    
    class Meta: 
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.usuario} - {self.lugar_de_inicio} a {self.lugar_de_fin}"
