from django.urls import path
from . import views

urlpatterns = [
    #AREA ADMINISTRATIVA DO USUARIO
    path('', views.index, name='index-account'),
    path('configuracoes/', views.configuracoes, name='configuracoes-account'),

    #AREA DE LOGIN / REGISTRE / LOGOUT
    path('registre/', views.registre, name='registre-account'),
    path('login/', views.logar, name='login-account'),
    path('logout/', views.deslogar, name='logout-account'),
]