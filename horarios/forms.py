from django import forms
from .models import Horario, AlumnoHorario

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia', 'hora_inicio', 'hora_fin', 'instructor']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'dia': 'Día',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
            'instructor': 'Instructor',
        }

class AlumnoHorarioForm(forms.ModelForm):
    class Meta:
        model = AlumnoHorario
        fields = ['alumno', 'horario']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'alumno': 'Alumno',
            'horario': 'Horario',
        }