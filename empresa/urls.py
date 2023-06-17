from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-empresa"),
    path("nova_empresa/", views.nova_empresa, name="nova_empresa-empresa"),
    path("editar/<int:id>/", views.editar_empresa),
    path("ativar/<int:id>/<str:acao>/", views.ativar),
    path("excluir/<int:id>/", views.excluir_empresa),
    # 3
    path("reuniao/", views.reuniao),
    path("calendario/", views.calendario),

]
