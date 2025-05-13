from django.db import models
# Create your models here.
from alumnos.models import Alumno  # Importas tu modelo desde la app alumnos

class Grado(models.Model):
    # Opciones para tipo de grado
    tipo = models.CharField(max_length=20)  # Ej: "kyū", "dan"
    nivel = models.PositiveIntegerField(help_text="Número del grado (ej: 10 para 10.º kyū, 1 para 1.º dan)")
    color = models.CharField(max_length=30)

    # Opciones para ámbito (local, nacional, etc.)
    AMBITO_CHOICES = [
        ('local', 'Local'),
        ('regional', 'Regional'),
        ('nacional', 'Nacional'),
        ('internacional', 'Internacional'),
    ]
    ambito = models.CharField(max_length=20, choices=AMBITO_CHOICES, blank=True, null=True)

    descripcion = models.TextField(blank=True, null=True)

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tipo', 'nivel']
        unique_together = ('tipo', 'nivel')

    def __str__(self):
        return f"{self.nivel}.º {self.tipo.capitalize()}: {self.color} ({self.get_ambito_display()})"

class HistorialGrado(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    fecha_obtencion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_obtencion']
        unique_together = ('alumno', 'grado')

    def __str__(self):
        return f"{self.alumno} - {self.grado.nombre} ({self.fecha_obtencion})"
