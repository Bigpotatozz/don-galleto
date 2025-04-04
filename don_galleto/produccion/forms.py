from django import forms
from .models import Merma_producto

class MermaRegistrarForm(forms.ModelForm):
    
    class Meta:
        model = Merma_producto
        fields = ['cantidad', 'motivo']
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ingrese la cantidad de merma"}),
            "motivo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese el motivo"}),
        }

