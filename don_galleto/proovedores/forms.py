from django import forms
from proovedores import models

class ProovedorRegistrarForm(forms.Form):
    nombre = forms.CharField(max_length=30, label='Nombre')
    nombre_contacto = forms.CharField(max_length=30, label='Nombre de contacto')
    telefono = forms.CharField(max_length=12, label='Telefono')
    correo = forms.EmailField(max_length=45, label='Correo')
    direccion = forms.CharField(max_length=100, label='Direccion')
    ciudad = forms.CharField(max_length=15, label='Ciudad')
    estado = forms.CharField(max_length=15, label='Estado')
    codigo_postal = forms.CharField(max_length=7, label='Codigo postal')
    estatus = forms.ChoiceField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo'), ('bloqueado', 'Bloqueado')])
    
    class Meta:
        model = models.Proovedor
        fields = ['nombre', 'nombre_contacto', 'telefono', 'correo', 'direccion', 'ciudad', 'estado', 'codigo_postal', 'estatus']
    
    def save(self):
        proovedor = models.Proovedor(
            nombre = self.cleaned_data['nombre'],
            nombre_contacto = self.cleaned_data['nombre_contacto'],
            telefono = self.cleaned_data['telefono'],
            correo = self.cleaned_data['correo'],
            direccion = self.cleaned_data['direccion'],
            ciudad = self.cleaned_data['ciudad'],
            estado = self.cleaned_data['estado'],
            codigo_postal = self.cleaned_data['codigo_postal'],
            estatus = self.cleaned_data['estatus']
        )
        proovedor.save()