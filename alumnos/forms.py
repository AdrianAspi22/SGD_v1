# alumnos/forms.py

from django import forms
from .models import Alumno
from datetime import date
from django.core.exceptions import ValidationError

class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Alumno
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento',
            'matricula', 'grupo', 'estado'
        ]

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if edad < 5:
            raise ValidationError('El alumno no puede ser menor de 5 años.')
        elif edad > 60:
            raise ValidationError('El alumno no puede ser mayor de 60 años.')

        return fecha_nacimiento


