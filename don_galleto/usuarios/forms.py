from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm

class Registro_admin_form(UserCreationForm):
        
        telefono = forms.CharField(max_length=10)
        rol = forms.ChoiceField(choices=[('empleado', 'Empleado'), ('cliente', 'Cliente'), ('admin', 'admin')])
        
        class Meta: 
            model = Usuario
            fields = ['username', 'email', 'password1', 'password2', 'telefono', 'rol']
            
            
            

class Edicion_usuario_form(forms.ModelForm):
      
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    contrasenia = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    telefono = forms.CharField(max_length=10)
    rol = forms.ChoiceField(choices=[('empleado', 'Empleado'), ('cliente', 'Cliente'), ('admin', 'admin')])
    is_active = forms.BooleanField(required=False, initial=True)


    class Meta:
          model = Usuario
          fields = ['username', 'email', 'contrasenia', 'telefono', 'rol', 'is_active']

    def save(self, id):
        
        usuario = Usuario.objects.get(id_usuario=id)
        usuario.username = self.cleaned_data['username']
        usuario.email = self.cleaned_data['email']
        usuario.telefono = self.cleaned_data['telefono']
        usuario.rol = self.cleaned_data['rol']
        nueva_contrasena = self.cleaned_data.get('contrasenia')
        usuario.is_active = self.cleaned_data['is_active']

        if nueva_contrasena:
             usuario.set_password(nueva_contrasena)
        
        usuario.save()
        return usuario