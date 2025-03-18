from django import forms
from usuarios.models import Usuario

class Form_editar_usuario(forms.ModelForm):
    nombre = forms.CharField(max_length=30)
    telefono = forms.CharField(max_length=10)
    correo = forms.EmailField(max_length=60)
    rol = forms.ChoiceField(choices=[('empleado', 'empleado'), ('cliente', 'cliente')])
    contrasenia = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'telefono', 'correo', 'contrasenia', 'rol']
        
    def save(self, id):
        
        contrasenia = self.cleaned_data['contrasenia'].encode('utf-8')
        salt  =  bcrypt.gensalt()
        contrasenia_hashed = bcrypt.hashpw(contrasenia, salt)
        
        edited_user = Usuario.objects.get(id_usuario=id)
        edited_user.telefono = self.cleaned_data['telefono']
        edited_user.rol = self.cleaned_data['rol']
        if self.cleaned_data['contrasenia'] != '':
            edited_user.contrasenia = contrasenia_hashed.decode('utf-8')
        edited_user.save()
        

        
