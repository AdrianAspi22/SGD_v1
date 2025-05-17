from django import forms
from .models import Instructor

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['nombres', 'apellidos', 'dni', 'telefono', 'correo', 'pago_hora']
