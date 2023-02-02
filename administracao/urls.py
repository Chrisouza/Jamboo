from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-administracao'),
    path('nova_empresa/', views.nova_empresa, name='nova_empresa-administracao'),
    path('novo_usuario/', views.novo_usuario, name="novo_usuario-administracao"),
    path('excluir/<int:id>/', views.excluir_empresa),
]