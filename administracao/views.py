from django.shortcuts import render, redirect
from empresa.models import Login, Nivel, Empresa
from django.contrib.auth.models import User
from .forms import FormNovoUsuario


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        logins = Login.objects.all()
        context = {
            "empresas": empresas,
            "logins": logins
        }
        return render(request, "administracao/public/home.html", context)
    return redirect("/")


def novo_usuario(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoUsuario(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                usuario = request.POST.get("usuario")
                senha = request.POST.get("senha")
                empresa = request.POST.get("empresa")
                nivel = request.POST.get("nivel")
                user = User.objects.create_user(
                    username=usuario, password=senha, email="")
                emp = Empresa.objects.get(id=empresa)
                nivel = Nivel.objects.get(id=nivel)
                Login.objects.create(usuario=user, empresa=emp, nivel=nivel)
                return redirect("/administracao/")
        context = {"form": form}
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")
