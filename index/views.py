from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import FormLogin
from django.contrib import messages


def alterar_senha(request):
    pass

def entrar(request):
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
            auth = authenticate(username=usuario, password=senha)
            if auth is not None:
                login(request, auth)
                messages.add_message(request, messages.INFO,
                                     "Login realizado com sucesso!")
                if auth.is_superuser:
                    return redirect("/administracao/")
                else:
                    return redirect("/empresa/")
    context = {"form_login": form_login}
    return render(request, "index/public/login.html", context)


def sair(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.WARNING,
                             "Logout realizado com sucesso!")
    return redirect("/")
