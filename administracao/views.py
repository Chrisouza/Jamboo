from django.shortcuts import render, redirect
from empresa.models import Login, Nivel, Empresa, Projeto
from django.contrib.auth.models import User
from .forms import FormNovoUsuario, FormNovoProjeto


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

##########################################################
############## GERENCIAMENTO DE USUARIOS #################
##########################################################
def gerenciar_usuarios(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(
            empresa=Empresa.objects.get(slug=slug).id)
        context = {
            "slug": slug,
            "logins": logins
        }
        return render(request, "administracao/public/gerenciar-usuario.html", context)
    return redirect("/")


def novo_usuario(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoUsuario(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                usuario = request.POST.get("usuario")
                senha = request.POST.get("senha")
                nivel = request.POST.get("nivel")
                user = User.objects.create_user(
                    username=usuario, password=senha, email="")
                emp = Empresa.objects.get(slug=slug)
                nivel = Nivel.objects.get(id=nivel)
                Login.objects.create(usuario=user, empresa=emp, nivel=nivel)
                return redirect("/administracao/")
        context = {"form": form, "slug": slug}
        return render(request, "administracao/public/novo-usuario.html", context)
    return redirect("/")

##########################################################
############# GERENCIAMENTO DE PROJETOS ##################
##########################################################
def gerenciar_projetos(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        projetos = Projeto.objects.filter(
            empresa=(Empresa.objects.get(slug=slug).id)
        )
        print(projetos)
        context = {
            "slug": slug,
            "projetos": projetos
        }
        return render(request, "administracao/public/gerenciar-projetos.html", context)
    return redirect("/")


def novo_projeto(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoProjeto(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                nome = request.POST.get("nome")
                slug_projeto = nome.replace(" ", "-")
                emp = Empresa.objects.get(slug=slug)
                Projeto.objects.create(
                    slug=slug_projeto, nome=nome, empresa=emp)
                return redirect("/administracao/")
        context = {"form": form, "slug": slug}
        return render(request, "administracao/public/novo-projeto.html", context)
    return redirect("/")

##########################################################
############# GERENCIAMENTO DE ARQUIVOS ##################
##########################################################
