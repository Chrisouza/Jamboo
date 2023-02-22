from django.shortcuts import render, redirect
from .models import Login, Level
from empresa.models import Company
from django.contrib.auth.models import User
from .forms import FormNewUser


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Company.objects.all()
        logins = Login.objects.all()
        context = {
            "empresas": empresas,
            "logins": logins
        }
        return render(request, "administracao/public/home.html", context)
    return redirect("/")


def novo_usuario(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNewUser(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username = request.POST.get("username")
                password = request.POST.get("password")
                empresa = request.POST.get("company")
                nivel = request.POST.get("level")
                user = User.objects.create_user(
                    username=username, password=password, email="")
                emp = Company.objects.get(id=empresa)
                nivel = Level.objects.get(id=nivel)
                Login.objects.create(user=user, company=emp, level=nivel)
                return redirect("/administracao/")
        context = {"form": form}
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")
