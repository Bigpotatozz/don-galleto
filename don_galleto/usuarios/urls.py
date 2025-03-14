
from django.urls import path
from . import views
from don_galleto.views import IndexView
from usuarios.views import Registro_view, Login_view
urlpatterns = [
    path('registrarse/', views.Registro_view.as_view(), name='registro'),
    path('login/', views.Login_view.as_view(), name = 'login')
]
