
from django.urls import path
from . import views
from don_galleto.views import IndexView
from usuarios.views import  Lista_usuarios_view, Editar_usuario_view
urlpatterns = [
    path('listado_usuarios/', views.Lista_usuarios_view.as_view(), name='listado_usuarios'),
    path('editar_usuario/<int:id>', views.Editar_usuario_view.as_view(), name='editar_usuario'),
  
]
