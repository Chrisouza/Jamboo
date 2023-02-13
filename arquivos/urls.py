from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.index),
    path('novo_arquivo/<int:id>/', views.novo_arquivo),
    path('<int:id_emp>/excluir/<str:nome_arquivo>/', views.excluir_arquivo),
]