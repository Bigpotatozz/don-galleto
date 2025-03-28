from django import forms
from .models import Galleta, Detalle_receta

class GalletaForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_receta', 'peso_unidad', 'duracion_promedio']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la galleta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la galleta'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de venta'}),
            'cantidad_receta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en receta'}),
            'peso_unidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso por unidad (g)'}),
            'duracion_promedio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración promedio (días)'}),
        }
class DetalleRecetaForm(forms.ModelForm):
    class Meta:
        model = Detalle_receta
        fields = ['id_insumo', 'cantidad']
        
        widgets = {
            'id_insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad del insumo'}),
        }

class GalletaEditarForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_receta', 'peso_unidad', 'duracion_promedio']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la galleta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la galleta'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de venta'}),
            'cantidad_receta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en receta'}),
            'peso_unidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso por unidad (g)'}),
            'duracion_promedio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración promedio (días)'}),
        }
        
    def save(self, id):
        galleta = Galleta.objects.filter(id_galleta=id).first()
        galleta.nombre = self.cleaned_data['nombre']
        galleta.descripcion = self.cleaned_data['descripcion']
        galleta.precio_venta = self.cleaned_data['precio_venta']
        galleta.cantidad_receta = self.cleaned_data['cantidad_receta']
        galleta.peso_unidad = self.cleaned_data['peso_unidad']
        galleta.duracion_promedio = self.cleaned_data['duracion_promedio']
        galleta.save()        

