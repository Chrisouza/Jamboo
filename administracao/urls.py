from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-administracao"),

    # gerencia niveis
    path("niveis/", views.gerenciar_niveis),
    path("niveis/novo/", views.novo_nivel),
    path("niveis/excluir/<int:nivel>/", views.excluir_nivel),

    # gerencia usuarios
    path("usuarios/<str:slug>/", views.gerenciar_usuarios),
    path("usuarios/<str:slug>/novo/", views.novo_usuario),
    path("usuarios/<str:slug>/<int:usuario>/", views.remove_usuario),

    # gernecia projetos
    path("projetos/<str:slug>/", views.gerenciar_projetos),
    path("projetos/<str:slug>/novo/", views.novo_projeto),
    path("projetos/<str:slug>/<int:projeto>/", views.remove_projeto),

    # gernecia arquivos
    path("arquivos/<str:slug>/", views.gerenciar_arquivos),
    path("arquivos/<str:slug>/<str:projeto>/novo/", views.novo_arquivo),
    path("arquivos/<str:slug>/<str:projeto>/excluir/<int:id_file>/",
         views.excluir_arquivo),
]
