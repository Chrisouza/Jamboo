from django.shortcuts import render, redirect

from .models import Empresa, Login
from django.contrib.auth.models import User

from .forms import FormNovaEmpresa, FormNovoUsuario

def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        context = {
            "empresas": empresas
        }
        return render(request, "administracao/public/home.html", context)
    return redirect("/")

def nova_empresa(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form  = FormNovaEmpresa(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                nome = request.POST.get("nome")
                slug = nome.replace(" ","-")
                telefone = request.POST.get("telefone")
                Empresa.objects.create(slug=slug, nome=nome, telefone=telefone)
                return redirect("/administracao/")
        context = {
            'form':form
        }
        return render(request, "administracao/public/nova_empresa.html", context)
    return redirect("/")

def novo_usuario(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form  = FormNovoUsuario(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username =  request.POST.get('username')
                password =  request.POST.get('password')
                enterprise = request.POST.get('enterprise')
                user = User.objects.create_user(username=username, password=password, email="")
                Login.objects.create(user_id=user.pk, enterprise_id=enterprise)
                return redirect("/administracao/")
        context = {
            'form':form
        }
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")

def excluir_empresa(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        Empresa.objects.filter(id=id).delete()
        return redirect("/administracao/")
    return redirect("/")