from django.db import models
from dojos.models import Dojo


class Instructor(models.Model):
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name='instructores')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    pago_hora = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
