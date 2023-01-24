from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-account'),
    path('registre/', views.registre, name='registre-account'),
    path('login/', views.logar, name='login-account'),
]