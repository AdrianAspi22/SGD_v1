from django import forms
from .models import Grado,HistorialGrado

class GradoForm(forms.ModelForm):

    
    class Meta:
        model = Grado
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
        fields = ['tipo', 'nivel', 'color', 'ambito', 'descripcion', 'estado']
        


class HistorialGradoForm(forms.ModelForm):
    fecha_obtencion = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'})
        )
    class Meta:
        model = HistorialGrado
        
        fields = ['alumno', 'grado', 'fecha_obtencion', 'observaciones']