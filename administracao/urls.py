from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("notificacoes/", views.notificacoes),

    # gerencia niveis
    path("niveis/", views.gerenciar_niveis),
    path("niveis/novo/", views.novo_nivel),
    path("niveis/excluir/<int:nivel>/", views.excluir_nivel),

    # gerencia usuarios
    path("usuarios/<str:slug_da_empresa>/", views.gerenciar_usuarios),
    path("usuarios/<str:slug_da_empresa>/novo/", views.novo_usuario),
    path("usuarios/<str:slug_da_empresa>/<int:usuario>/", views.remove_usuario),

    # gernecia projetos
    path("projetos/<str:slug_da_empresa>/", views.gerenciar_projetos),
    path("projetos/<str:slug_da_empresa>/novo/", views.novo_projeto),
    path("projetos/<str:slug_da_empresa>/<int:projeto>/", views.remove_projeto),

    # gernecia arquivos
    path("arquivos/<str:slug_da_empresa>/", views.gerenciar_arquivos),
    path("arquivos/<str:slug_da_empresa>/<str:projeto>/novo/", views.novo_arquivo),
    path("arquivos/<str:slug_da_empresa>/<str:projeto>/excluir/<int:id_file>/", views.excluir_arquivo),
    path("arquivos/<str:slug_da_empresa>/<str:projeto>/ver/", views.ver_arquivos),
]
