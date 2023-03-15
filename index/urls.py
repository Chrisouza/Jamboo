from django.urls import path
from . import views

urlpatterns = [
    path("", views.entrar, name="login-index"),
    path("logout/", views.sair, name="logout-index"),
]
