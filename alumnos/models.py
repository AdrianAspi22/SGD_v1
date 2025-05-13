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


    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name='alumnos')

    # Campos nuevos
    matricula = models.CharField(max_length=30, choices=MATRÍCULA_CHOICES, default='Matricula regular')
    grupo = models.CharField(max_length=20, choices=GRUPO_CHOICES, default='Mañana')
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

