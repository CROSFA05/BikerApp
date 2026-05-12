from django.test import TestCase, Client
from django.urls import reverse
from django.middleware.csrf import get_token
from miApp.models import Usuario, GrupoBiker, Vehiculo, ContactoEmergencia, Viaje, UsuarioVehiculo
from datetime import date

class UsuarioFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.grupo = GrupoBiker.objects.create(nombre='Test Group', descripcion='Test', activo=True)
        cls.vehiculo = Vehiculo.objects.create(marca='Honda', modelo='CBR', año=2020, color='Rojo', matricula='ABC123', tipo_vehiculo=0)

    def test_fecha_nacimiento_string_value(self):
        from miApp.forms import UsuarioForm
        form = UsuarioForm(data={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'fecha_nacimiento': '1995-06-15',
            'sexo': '1',
            'rol': '0',
            'grupo_biker': str(self.grupo.id),
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())
        user = form.save()
        self.assertEqual(user.fecha_nacimiento, date(1995, 6, 15))

    def test_fecha_nacimiento_empty(self):
        from miApp.forms import UsuarioForm
        form = UsuarioForm(data={
            'email': 'test2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'sexo': '0',
            'rol': '0',
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_vehiculos_assignment(self):
        from miApp.forms import UsuarioForm
        form = UsuarioForm(data={
            'email': 'test3@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'fecha_nacimiento': '1995-06-15',
            'sexo': '1',
            'rol': '0',
            'vehiculos': [self.vehiculo.id],
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())
        user = form.save()
        self.assertEqual(user.email, 'test3@example.com')
        self.assertIn(self.vehiculo, form.cleaned_data['vehiculos'])

    def test_fecha_nacimiento_widget_renders_correct_format(self):
        from miApp.forms import UsuarioForm
        form = UsuarioForm()
        widget = form.fields['fecha_nacimiento'].widget
        rendered = widget.render('fecha_nacimiento', date(1995, 6, 15))
        self.assertIn('value="1995-06-15"', rendered)
        rendered_str = widget.render('fecha_nacimiento', '1995-06-15')
        self.assertIn('value="1995-06-15"', rendered_str)

    def test_grupo_biker_queryset_active_only(self):
        from miApp.forms import UsuarioForm
        GrupoBiker.objects.create(nombre='Inactive Group', descripcion='Test', activo=False)
        form = UsuarioForm()
        opts = list(form.fields['grupo_biker'].queryset.values_list('id', flat=True))
        self.assertIn(self.grupo.id, opts)
        self.assertEqual(form.fields['grupo_biker'].queryset.count(), 1)

    def test_optional_fields_not_required(self):
        from miApp.forms import UsuarioForm
        form = UsuarioForm(data={
            'email': 'minimal@test.com',
            'first_name': 'Minimal',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'sexo': '',
            'rol': '',
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())


class UsuarioChangeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.grupo = GrupoBiker.objects.create(nombre='Test Group 2', descripcion='Test', activo=True)
        cls.vehiculo = Vehiculo.objects.create(marca='Yamaha', modelo='R6', año=2019, color='Azul', matricula='XYZ789', tipo_vehiculo=0)
        cls.user = Usuario.objects.create_user(email='change@example.com', password='testpass123', first_name='Change', last_name='User')
        cls.user.fecha_nacimiento = date(1990, 1, 1)
        cls.user.save()
        UsuarioVehiculo.objects.create(usuario=cls.user, vehiculo=cls.vehiculo)

    def test_fecha_nacimiento_widget_renders_date_object(self):
        from miApp.forms import UsuarioChangeForm
        form = UsuarioChangeForm(instance=self.user)
        widget = form.fields['fecha_nacimiento'].widget
        rendered = widget.render('fecha_nacimiento', date(1990, 1, 1))
        self.assertIn('value="1990-01-01"', rendered)

    def test_vehiculos_initial_from_instance(self):
        from miApp.forms import UsuarioChangeForm
        form = UsuarioChangeForm(instance=self.user)
        initial_vehs = list(form.fields['vehiculos'].initial or [])
        self.assertEqual(len(initial_vehs), 1)
        self.assertEqual(initial_vehs[0], self.vehiculo)

    def test_optional_fields_not_required(self):
        from miApp.forms import UsuarioChangeForm
        form = UsuarioChangeForm(instance=self.user, data={
            'email': 'change@example.com',
            'first_name': 'Changed',
            'last_name': 'User',
            'sexo': '',
            'rol': '',
            'is_active': True,
            'is_staff': False,
            'grupo_biker': str(self.grupo.id),
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())


class ViewIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user(email='admin@test.com', password='testpass123', first_name='Admin', last_name='User', is_staff=True)
        cls.grupo = GrupoBiker.objects.create(nombre='Test Grupo', descripcion='Test', activo=True)
        cls.vehiculo = Vehiculo.objects.create(marca='Kawasaki', modelo='Ninja', año=2021, color='Verde', matricula='NINJA123', tipo_vehiculo=0)
        cls.vehiculo2 = Vehiculo.objects.create(marca='Ducati', modelo='Panigale', año=2022, color='Rojo', matricula='DUCA456', tipo_vehiculo=0)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin)

    def test_usuario_alta_saves_all_fields(self):
        response = self.client.post(reverse('usuarioAlta'), {
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'telefono': '1234567890',
            'fecha_nacimiento': '1995-06-15',
            'sexo': '1',
            'tipo_de_sangre': '0',
            'enfermedades': 'Ninguna',
            'alergias': 'Ninguna',
            'nss': '12345678901',
            'poliza_seguro': 'POL123',
            'aseguradora': 'Seguros Test',
            'grupo_biker': str(self.grupo.id),
            'rol': '0',
            'activo': True,
            'vehiculos': [self.vehiculo.id],
        })
        self.assertEqual(response.status_code, 302)
        user = Usuario.objects.get(email='newuser@test.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.fecha_nacimiento, date(1995, 6, 15))
        self.assertEqual(user.vehiculos.count(), 1)
        self.assertEqual(user.vehiculos.first(), self.vehiculo)

    def test_usuario_editar_updates_all_fields(self):
        user = Usuario.objects.create_user(email='edituser@test.com', password='testpass123', first_name='Edit', last_name='User')
        user.fecha_nacimiento = date(1990, 1, 1)
        user.save()
        UsuarioVehiculo.objects.create(usuario=user, vehiculo=self.vehiculo)

        response = self.client.post(reverse('usuarioEditar', args=[user.id]), {
            'email': 'edituser@test.com',
            'first_name': 'Editado',
            'last_name': 'Usuario',
            'telefono': '9876543210',
            'fecha_nacimiento': '1992-12-25',
            'sexo': '2',
            'tipo_de_sangre': '6',
            'enfermedades': 'Test disease',
            'alergias': 'Test allergy',
            'nss': '98765432109',
            'poliza_seguro': 'POL999',
            'aseguradora': 'Seguros Edit',
            'grupo_biker': str(self.grupo.id),
            'rol': '1',
            'activo': True,
            'is_active': True,
            'is_staff': False,
            'vehiculos': [self.vehiculo2.id],
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Editado')
        self.assertEqual(user.fecha_nacimiento, date(1992, 12, 25))
        self.assertEqual(user.vehiculos.count(), 1)
        self.assertEqual(user.vehiculos.first(), self.vehiculo2)

    def test_usuario_editar_preserves_grupo_biker(self):
        user = Usuario.objects.create_user(email='grupouser@test.com', password='testpass123', first_name='Grupo', last_name='User')
        user.grupo_biker = self.grupo
        user.save()

        self.client.post(reverse('usuarioEditar', args=[user.id]), {
            'email': 'grupouser@test.com',
            'first_name': 'Grupo',
            'last_name': 'User',
            'telefono': '',
            'fecha_nacimiento': '',
            'sexo': '0',
            'tipo_de_sangre': '',
            'enfermedades': '',
            'alergias': '',
            'nss': '',
            'poliza_seguro': '',
            'aseguradora': '',
            'grupo_biker': str(self.grupo.id),
            'rol': '0',
            'activo': True,
            'is_active': True,
            'is_staff': False,
            'vehiculos': [],
        })
        user.refresh_from_db()
        self.assertEqual(user.grupo_biker, self.grupo)

    def test_usuario_editar_clears_vehiculos(self):
        user = Usuario.objects.create_user(email='clearveh@test.com', password='testpass123', first_name='Clear', last_name='Veh')
        user.save()
        UsuarioVehiculo.objects.create(usuario=user, vehiculo=self.vehiculo)
        self.assertEqual(user.vehiculos.count(), 1)

        self.client.post(reverse('usuarioEditar', args=[user.id]), {
            'email': 'clearveh@test.com',
            'first_name': 'Clear',
            'last_name': 'Veh',
            'telefono': '',
            'fecha_nacimiento': '',
            'sexo': '0',
            'tipo_de_sangre': '',
            'enfermedades': '',
            'alergias': '',
            'nss': '',
            'poliza_seguro': '',
            'aseguradora': '',
            'grupo_biker': '',
            'rol': '0',
            'activo': True,
            'is_active': True,
            'is_staff': False,
            'vehiculos': [],
        })
        user.refresh_from_db()
        self.assertEqual(user.vehiculos.count(), 0)


class NavigationPersistTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user(email='navadmin@test.com', password='testpass123', first_name='Nav', last_name='Admin', is_staff=True)
        cls.grupo = GrupoBiker.objects.create(nombre='Nav Grupo', descripcion='Test', activo=True)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin)

    def test_change_then_navigate_saves(self):
        user = Usuario.objects.create_user(email='navuser@test.com', password='testpass123', first_name='NavUser', last_name='Test')
        user.fecha_nacimiento = date(1990, 1, 1)
        user.save()

        self.client.post(reverse('usuarioEditar', args=[user.id]), {
            'email': 'navuser@test.com',
            'first_name': 'NavUserChanged',
            'last_name': 'Test',
            'telefono': '1234567890',
            'fecha_nacimiento': '1995-06-15',
            'sexo': '1',
            'tipo_de_sangre': '0',
            'enfermedades': '',
            'alergias': '',
            'nss': '',
            'poliza_seguro': '',
            'aseguradora': '',
            'grupo_biker': str(self.grupo.id),
            'rol': '0',
            'activo': True,
            'is_active': True,
            'is_staff': False,
            'vehiculos': [],
        })

        response = self.client.get(reverse('usuarios'))
        self.assertContains(response, 'NavUserChanged', status_code=200)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'NavUserChanged')
        self.assertEqual(user.fecha_nacimiento, date(1995, 6, 15))

    def test_multiple_edits_persist(self):
        user = Usuario.objects.create_user(email='multi@test.com', password='testpass123', first_name='Multi', last_name='User')
        user.fecha_nacimiento = date(1990, 1, 1)
        user.save()

        for i in range(3):
            self.client.post(reverse('usuarioEditar', args=[user.id]), {
                'email': 'multi@test.com',
                'first_name': f'Multi{i}',
                'last_name': 'User',
                'telefono': '',
                'fecha_nacimiento': f'199{i}-01-01',
                'sexo': '0',
                'tipo_de_sangre': '',
                'enfermedades': '',
                'alergias': '',
                'nss': '',
                'poliza_seguro': '',
                'aseguradora': '',
                'grupo_biker': '',
                'rol': '0',
                'activo': True,
                'is_active': True,
                'is_staff': False,
                'vehiculos': [],
            })
            user.refresh_from_db()
            self.assertEqual(user.first_name, f'Multi{i}')

    def test_vehiculos_show_in_usuario_list(self):
        user = Usuario.objects.create_user(email='vehusers@test.com', password='testpass123', first_name='Vech', last_name='User')
        user.grupo_biker = self.grupo
        user.save()
        v = Vehiculo.objects.create(marca='Suzuki', modelo='Hayabusa', año=2020, color='Negro', matricula='SUZI123', tipo_vehiculo=0)
        UsuarioVehiculo.objects.create(usuario=user, vehiculo=v)

        response = self.client.get(reverse('usuarios'))
        self.assertContains(response, 'Suzuki', status_code=200)

    def test_usuario_detalle_shows_vehiculos(self):
        user = Usuario.objects.create_user(email='detvehs@test.com', password='testpass123', first_name='Det', last_name='User')
        user.grupo_biker = self.grupo
        user.save()
        v = Vehiculo.objects.create(marca='BMW', modelo='S1000RR', año=2021, color='Blanco', matricula='BMW1234', tipo_vehiculo=0)
        UsuarioVehiculo.objects.create(usuario=user, vehiculo=v)

        response = self.client.get(reverse('usuarioDetalle', args=[user.id]))
        self.assertContains(response, 'BMW', status_code=200)