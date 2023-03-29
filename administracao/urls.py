from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-administracao"),
    path("novo_usuario/", views.novo_usuario,
         name="novo_usuario-administracao"),
]
