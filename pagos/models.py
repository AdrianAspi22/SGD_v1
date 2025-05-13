from django.db import models
from dojos.models import Dojo  # Importamos el modelo Dojo
from alumnos.models import Alumno  # Importamos el modelo Alumno
from decimal import Decimal
from instructores.models import Instructor  # Ajusta si está en otro módulo

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.CharField(max_length=100)
    fecha_pago = models.DateTimeField()
    estado = models.BooleanField(default=True)
    estado_pago = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name='pagos')

    def __str__(self):
        return f"Pago de {self.alumno} por {self.concepto}"


class PagoInstructor(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    
    # Semana de trabajo
    semana_inicio = models.DateField(help_text="Lunes de la semana trabajada")
    semana_fin = models.DateField(help_text="Domingo de la semana trabajada")

    fecha_pago = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]
    estado_pago = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, related_name='pagos_instructor')

    estado = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pago semanal a {self.instructor} - S/. {self.monto} ({self.semana_inicio} a {self.semana_fin})"
