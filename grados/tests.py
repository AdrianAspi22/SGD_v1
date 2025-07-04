from django.test import TestCase
from datetime import date, timedelta
from grados.models import Grado, HistorialGrado
from alumnos.models import Alumno
from dojos.models import Dojo
from usuarios.models import Usuario
from grados.services import promover_si_corresponde

class PromoverSiCorrespondeTests(TestCase):
    def setUp(self):
        # Obtener o crear el usuario asociado al dojo
        self.usuario, created = Usuario.objects.get_or_create(
            username='admin_dojo',
            defaults={
                'password': 'admin123',
                'tipo': 'dojo',
                'is_staff': True,
                'is_superuser': True,
                'estado': True
            }
        )

        # Crear el dojo
        self.dojo = Dojo.objects.create(
            nombre="Dojo Central",
            descripcion="Dojo de pruebas",
            ubicacion="Ciudad X",
            usuario=self.usuario
        )

        # Crear grados
        self.grado1 = Grado.objects.create(tipo="kyū", nivel=1, color="blanco", dojo=self.dojo)
        self.grado2 = Grado.objects.create(tipo="kyū", nivel=2, color="amarillo", dojo=self.dojo)
        self.grado3 = Grado.objects.create(tipo="kyū", nivel=3, color="naranja", dojo=self.dojo)

        # Crear alumno válido
        self.alumno = Alumno.objects.create(
            nombre="Juan",
            apellido="Pérez",
            fecha_nacimiento="2000-01-01",
            dojo=self.dojo
        )

    def test_sin_historial_actual(self):
        promover_si_corresponde(self.alumno)
        self.assertEqual(HistorialGrado.objects.filter(alumno=self.alumno).count(), 0)

    def test_siguiente_grado_no_existe(self):
        HistorialGrado.objects.create(alumno=self.alumno, grado=self.grado3, estado=True, fecha_obtencion=date.today())
        promover_si_corresponde(self.alumno)
        self.assertEqual(HistorialGrado.objects.filter(alumno=self.alumno).count(), 1)

    def test_historial_ya_tiene_siguiente_grado(self):
        HistorialGrado.objects.create(alumno=self.alumno, grado=self.grado1, estado=True, fecha_obtencion=date.today())
        HistorialGrado.objects.create(alumno=self.alumno, grado=self.grado2, estado=False, fecha_obtencion=date.today() - timedelta(days=100))
        promover_si_corresponde(self.alumno)
        self.assertEqual(HistorialGrado.objects.filter(alumno=self.alumno, grado=self.grado2).count(), 1)

    def test_promocion_exitosa(self):
        HistorialGrado.objects.create(alumno=self.alumno, grado=self.grado1, estado=True, fecha_obtencion=date.today())
        promover_si_corresponde(self.alumno)
        self.assertTrue(HistorialGrado.objects.filter(alumno=self.alumno, grado=self.grado2).exists())
