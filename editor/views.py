from django.shortcuts import render, redirect
from empresa.models import Empresa
from index.auxiliar import pega_notificacoes, aviso
from index.forms import FormEditor
from index.mensagens import info


def index(request):
    if request.user.is_authenticated:
        form = FormEditor()
        empresas = Empresa.objects.all()
        notificacoes = pega_notificacoes(request=request)
        context = {"empresas": empresas, "notificacoes": notificacoes, "aviso": aviso(request), "form":form}
        return render(request, "editor/public/home.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")