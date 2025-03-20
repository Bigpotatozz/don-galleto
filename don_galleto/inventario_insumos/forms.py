from django import forms
from inventario_insumos.models import Insumo

class Registro_insumo_form(forms.ModelForm):
    nombre = forms.CharField(max_length=45)
    tipo = forms.ChoiceField(choices=[('base', 'Base'), ('complemento', 'Complemento')])
    tipo_medida = forms.ChoiceField(choices=[('gramos', 'Gramos'), ('mililitros', 'Mililitros')])
    
    class Meta:
        model = Insumo
        fields = ['nombre', 'tipo', 'tipo_medida']
        
    def save(self):
        nombre = self.cleaned_data['nombre']
        tipo = self.cleaned_data['tipo']
        tipo_medida = self.cleaned_data['tipo_medida']
        
        new_insumo = Insumo(nombre=nombre, tipo=tipo, tipo_medida=tipo_medida, cantidad = 0, estatus = 'sin existencias')
        new_insumo.save()

        
        