from django import forms
from usuarios.models import Usuario


class Form_registrar_usuario(forms.ModelForm):
    
    nombre = forms.CharField(max_length=30)
    telefono = forms.CharField(max_length=10)
    correo = forms.EmailField(max_length=60)
    contrasenia = forms.CharField(max_length=45, widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=[('empleado', 'empleado'), ('cliente', 'cliente')])
    
    class Meta: 
        model = Usuario
        fields = ['nombre', 'telefono', 'correo', 'contrasenia', 'rol']
        
    def save(self):
        new_user = Usuario(nombre = self.cleaned_data['nombre'],
                            telefono = self.cleaned_data['telefono'],
                            correo = self.cleaned_data['correo'],
                            contrasenia = self.cleaned_data['contrasenia'],
                            rol = self.cleaned_data['rol'],
                            codigo_verificacion = 0)
        new_user.save()