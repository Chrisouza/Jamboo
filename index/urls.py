from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index-index"),
    path("", views.entrar, name="login-index"),
    path("logout/", views.sair, name="logout-index"),
]
