from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-administracao"),
    #gerencia usuarios
    path("usuarios/<str:slug>/", views.gerenciar_usuarios),
    path("usuarios/<str:slug>/novo/", views.novo_usuario),
    #gernecia projetos
    path("projetos/<str:slug>/", views.gerenciar_projetos),
    path("projetos/<str:slug>/novo/", views.novo_projeto),
]