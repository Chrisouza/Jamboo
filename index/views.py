from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from .forms import FormLogin
from .mensagens import *

from empresa.models import Empresa, Login, Nivel


def inicia_admin():
    existe_adm = Nivel.objects.filter(id=1)
    if len(existe_adm) == 0:
        Nivel.objects.create(
            nome_do_nivel="administrador",
            descricao="administrador da empresa"
        )


def alterar_senha(request):
    pass


def entrar(request):
    inicia_admin()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/administracao/")
        else:
            return redirect("/empresa/")

    form_login = FormLogin(request.POST or None)
    if request.method == "POST":
        if form_login.is_valid():
            usuario = request.POST.get("usuario")
            senha = request.POST.get("senha")
            try:
                email = User.objects.get(email=usuario)
                auth = authenticate(username=email.username, password=senha)
            except:
                auth = authenticate(username=usuario, password=senha)
            if auth is not None:
                if not auth.is_superuser:
                    acesso = Login.objects.get(usuario=auth.id)
                    empresa = Empresa.objects.get(id=acesso.empresa.id)
                    if not empresa.ativo:
                        warning(request, msg="Você não tem permissao de acesso. Entre em contato!")
                        return redirect("/")
                login(request, auth)
                sucesso(request, msg="Login realizado com sucesso!")
                return redirect("/")
            else:
                warning(request, msg="Usuário/E-mail ou Senha incorretos!")
    context = {"form_login": form_login}
    return render(request, "index/public/login.html", context)


def sair(request):
    if request.user.is_authenticated:
        logout(request)
        info(request, msg="Logout realizado com sucesso!")
    return redirect("/")
