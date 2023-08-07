import logging
from django.shortcuts import render, redirect
from empresa.models import Arquivo, Login
from index.auxiliar import pega_notificacoes, aviso
from index.forms import FormEditor
from index.mensagens import info


def index(request, projeto):
    if request.user.is_authenticated:
        login = Login.objects.get(usuario=request.user)
        imagens = Arquivo.objects.filter(
            empresa=login.empresa, projeto=projeto)
        print(imagens)
        notificacoes = pega_notificacoes(request=request)
        context = {"empresas": login, "notificacoes": notificacoes,
                   "aviso": aviso(request), "imagens": imagens}
        return render(request, "editor/public/home.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")
