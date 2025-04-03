from django import forms
from django.core.exceptions import ValidationError
from .models import ItemCarrito  
from datetime import date

class AgregarAlCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ['galleta', 'cantidad', 'presentacion', 'fecha_recoger']
        widgets = {
            'galleta': forms.HiddenInput(),
            'fecha_recoger': forms.DateInput(attrs={
                'type': 'date', 
                'min': date.today().strftime('%Y-%m-%d')
            })
        }
    
    def clean_fecha_recoger(self):
        fecha = self.cleaned_data['fecha_recoger']
        if fecha < date.today():
            raise ValidationError("La fecha de recogida no puede ser en el pasado.")
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        galleta = cleaned_data.get('galleta')
        cantidad = cleaned_data.get('cantidad')
        presentacion = cleaned_data.get('presentacion')
        
        if galleta and cantidad and presentacion:
            if presentacion in ['700g', '1kg'] and not galleta.cantidad > 0:
                raise ValidationError(
                    f"No hay suficiente stock de {galleta.nombre} en la presentación seleccionada."
                )
        return cleaned_data

class ConfirmarPedidoForm(forms.Form):
    fecha_recoger = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': date.today().strftime('%Y-%m-%d')
        }),
        label="Fecha de recogida"
    )
    
    def clean_fecha_recoger(self):
        fecha = self.cleaned_data['fecha_recoger']
        if fecha < date.today():
            raise ValidationError("La fecha de recogida no puede ser en el pasado.")
        return fecha