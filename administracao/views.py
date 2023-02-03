import os
import shutil

from django.conf import settings
from django.shortcuts import render, redirect

from .models import Empresa, Login
from django.contrib.auth.models import User

from .forms import FormNovaEmpresa, FormNovoUsuario

folders = ['pdf', 'images', 'audios', 'videos']

def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        print(settings.BASE_DIR)
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
                emp = Empresa.objects.create(slug=slug, nome=nome, telefone=telefone)
                if emp:
                    os.mkdir(f"{settings.BASE_DIR}/media/{slug}")
                    for folder in folders:
                        os.mkdir(f"{settings.BASE_DIR}/media/{slug}/{folder}")
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
                level = request.POST.get('level')
                user = User.objects.create_user(username=username, password=password, email="")
                Login.objects.create(user_id=user.pk, enterprise_id=enterprise, level=level)
                return redirect("/administracao/")
        context = {
            'form':form
        }
        return render(request, "administracao/public/novo_usuario.html", context)
    return redirect("/")

def excluir_empresa(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(enterprise_id=id)
        for login in logins:
            User.objects.get(id=login.user_id).delete()
        emp = Empresa.objects.get(id=id)
        emp.delete()
        shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.slug}", ignore_errors=True)
        return redirect("/administracao/")
    return redirect("/")