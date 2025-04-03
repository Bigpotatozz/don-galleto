from usuarios.models import Usuario

def auth_context(request):
    
    user_id = request.session.get('id_usuario')
    
    if user_id:
        try:
            user = Usuario.objects.get(id_usuario=user_id)
            return {
                
                'is_authenticated': True,
                'user_rol': user.rol,
                'user_id': user.id_usuario,
            }
            
        except Usuario.DoesNotExist:
            pass
    
    return {
        'is_authenticated': False,
        'user_rol': None,
    }