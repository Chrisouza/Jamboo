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
                username = request.POST.get("username")
                password = request.POST.get("password")
                empresa = request.POST.get("company")
                nivel = request.POST.get("level")
                user = User.objects.create_user(
                    username=username, password=password, email="")
                emp = Empresa.objects.get(id=empresa)
                nivel = Nivel.objects.get(id=nivel)
                Login.objects.create(user=user, company=emp, level=nivel)
                return redirect("/administracao/")
        context = {"form": form}
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")
