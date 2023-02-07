from django.shortcuts import render, redirect
from .models import Login
from django.contrib.auth.models import User
from .forms import FormNovoUsuario
from empresa.models import Empresa


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        context = {
            "empresas": empresas
        }
        return render(request, "administracao/public/home.html", context)
    return redirect("/")

def novo_usuario(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form  = FormNovoUsuario(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username =  request.POST.get('username')
                password =  request.POST.get('password')
                empresa = request.POST.get('empresa')
                level = request.POST.get('level')
                user = User.objects.create_user(username=username, password=password, email="")
                Login.objects.create(user_id=user.pk, empresa=empresa, level=level)
                return redirect("/administracao/")
        context = {
            'form':form
        }
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")