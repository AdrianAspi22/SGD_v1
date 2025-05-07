# alumnos/forms.py

from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Alumno
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento',
            'matricula', 'grupo', 'cinturon', 'estado'
        ]
