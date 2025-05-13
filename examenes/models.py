# examenes/models.py
from horarios.models import Horario
from instructores.models import Instructor
from django.db import models
from alumnos.models import Alumno
from decimal import Decimal

class Examen(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)  # <-- Nuevo campo para la hora del examen
    nota_aprobacion = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10'))
    monto_pago = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))  # <-- campo nuevo
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class AlumnoExamen(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='examenes')
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='alumnos')
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aprobado = models.BooleanField(default=False)

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('alumno', 'examen')  # Para evitar duplicados

    def __str__(self):
        return f"{self.alumno} - {self.examen}"
