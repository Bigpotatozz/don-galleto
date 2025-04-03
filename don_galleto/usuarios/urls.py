
from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
from usuarios.views import  Lista_usuarios_view, Registro_admin_view, Edicion_usuario_view, eliminar_usuario
urlpatterns = [
    path('listado_usuarios/', login_required(views.Lista_usuarios_view.as_view()), name='listado_usuarios'),
    path('registro_admin/', views.Registro_admin_view.as_view(), name='registro_admin'),
    path('editar_usuario/<int:id>/', views.Edicion_usuario_view.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
]
