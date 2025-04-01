from django import forms
from .models import Venta, Galleta


class SelectGalletas(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nombre} - ${obj.precio_venta}"

class DetalleVentaForm(forms.Form):
    galletas = SelectGalletas(
        queryset=Galleta.objects.all(),
        label="Galletas",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    cantidad = forms.FloatField(
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    presentacion = forms.ChoiceField(
        choices=[('gr', 'Gramos'), ('unidad', 'Unidad'), ('paquete', 'Paquete')],
        label="Presentación",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class VentaRegistroForms(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha_venta', 'tipo']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}, choices=[('fisica', 'Física'), ('pedido', 'Pedido')]),
        }
