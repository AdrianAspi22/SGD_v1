# examenes/forms.py
from django import forms
from .models import Examen, AlumnoExamen
from grados.models import HistorialGrado

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            'titulo',
            'descripcion',
            'fecha',
            'hora',
            'nota_aprobacion',
            'monto_pago',
            'instructor',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }


class AlumnoExamenForm(forms.ModelForm):
    class Meta:
        model = AlumnoExamen
        fields = [
            'alumno',
            'examen',
        ]


class EvaluarExamenForm(forms.ModelForm):
    class Meta:
        model = AlumnoExamen
        fields = ['nota', 'observaciones']
