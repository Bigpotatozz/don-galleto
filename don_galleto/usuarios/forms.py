from django import forms
from usuarios.models import Usuario
import bcrypt


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
        
        contrasenia = self.cleaned_data['contrasenia'].encode('utf-8')
        salt  =  bcrypt.gensalt()
        contrasenia_hashed = bcrypt.hashpw(contrasenia, salt)
        new_user = Usuario(nombre = self.cleaned_data['nombre'],
                            telefono = self.cleaned_data['telefono'],
                            correo = self.cleaned_data['correo'],
                            contrasenia = contrasenia_hashed.decode('utf-8'),
                            rol = self.cleaned_data['rol'],
                            codigo_verificacion = 0)
        new_user.save()
        
        
class Form_iniciar_sesion(forms.ModelForm):
    
    correo = forms.EmailField(max_length=60)
    contrasenia = forms.CharField(max_length=45, widget=forms.PasswordInput)
    
    class Meta: 
        model = Usuario
        fields = ['correo', 'contrasenia']    
        
    def auth(self):
        try: 
            user = Usuario.objects.get(correo=self.cleaned_data['correo'])
            
            if(bcrypt.checkpw(self.cleaned_data['contrasenia'].encode('utf-8'), user.contrasenia.encode('utf-8'))):
                return user
            else: 
                return None
            
        #Maneja la excepcion si el usuario no llegara a existir
        except Usuario.DoesNotExist:
            return None

        
        
