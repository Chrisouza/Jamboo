from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.index, name="login"),
    path('registre/', views.registre, name="registre"),
    path('sair/', views.sair, name="sair"),
]
