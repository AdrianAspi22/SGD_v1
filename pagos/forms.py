# pagos/forms.py
from django import forms
from .models import Pago
from dojos.models import Dojo  # Importamos el modelo Dojo

class PagoForm(forms.ModelForm):
    fecha_pago = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Pago
        fields = ['alumno', 'concepto', 'monto', 'fecha_pago', 'estado_pago']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asignamos el dojo automáticamente al crear un pago
        if 'dojo' not in self.initial:
            self.initial['dojo'] = self.initial.get('user_dojo', None)

    def save(self, commit=True):
        pago = super().save(commit=False)
        # Asignamos el dojo del usuario autenticado
        pago.dojo = self.initial.get('dojo')
        if commit:
            pago.save()
        return pago
