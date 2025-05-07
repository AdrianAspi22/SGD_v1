# alumnos/models.py

from django.db import models
from dojos.models import Dojo  # si la app se llama dojos

class Alumno(models.Model):
    MATRÍCULA_CHOICES = [
        ('Matricula regular', 'Matrícula regular'),
        ('Matricula excepcional', 'Matrícula excepcional'),
    ]

    GRUPO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    CINTURON_CHOICES = [
        ('10.º kyū: Blanco', '10.º kyū: Blanco'),
        ('9.º kyū: Amarillo', '9.º kyū: Amarillo'),
        ('8.º kyū: Naranja', '8.º kyū: Naranja'),
        ('7.º kyū: Verde', '7.º kyū: Verde'),
        ('6.º kyū: Azul', '6.º kyū: Azul'),
        ('5.º kyū: Marrón', '5.º kyū: Marrón'),
        ('4.º kyū: Marrón', '4.º kyū: Marrón'),
        ('3.º kyū: Marrón', '3.º kyū: Marrón'),
        ('2.º kyū: Marrón', '2.º kyū: Marrón'),
        ('1.º kyū: Marrón', '1.º kyū: Marrón'),
        ('1.º dan: Cinturón negro', '1.º dan: Cinturón negro'),
        ('2.º dan: Cinturón negro', '2.º dan: Cinturón negro'),
        ('3.º dan: Cinturón negro', '3.º dan: Cinturón negro'),
        ('4.º dan: Cinturón negro', '4.º dan: Cinturón negro'),
        ('5.º dan: Cinturón negro', '5.º dan: Cinturón negro'),
        ('6.º dan: Cinturón negro', '6.º dan: Cinturón negro'),
        ('7.º dan: Cinturón negro', '7.º dan: Cinturón negro'),
        ('8.º dan: Cinturón negro', '8.º dan: Cinturón negro'),
        ('9.º dan: Cinturón negro', '9.º dan: Cinturón negro'),
        ('10.º dan: Cinturón negro', '10.º dan: Cinturón negro'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name='alumnos')

    # Campos nuevos
    matricula = models.CharField(max_length=30, choices=MATRÍCULA_CHOICES, default='Matricula regular')
    grupo = models.CharField(max_length=20, choices=GRUPO_CHOICES, default='Mañana')
    cinturon = models.CharField(max_length=50, choices=CINTURON_CHOICES, default='10.º kyū: Blanco')
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

