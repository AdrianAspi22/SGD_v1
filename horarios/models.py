from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from alumnos.models import Alumno
from instructores.models import Instructor

# horarios/models.py

class Horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='horarios')


    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin.")

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"


class AlumnoHorario(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='horarios')
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='alumnos')
    
    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('alumno', 'horario')

    def __str__(self):
        return f"{self.alumno.username} - {self.horario}"
