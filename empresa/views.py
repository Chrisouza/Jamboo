import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from empresa.models import Login, Empresa, Nivel
from django.contrib.auth.models import User
from .forms import FormNovaEmpresa
from .funcoes import cria_pasta


def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)
        context = {"empresa": empresa}
        return render(request, "empresa/public/home.html", context)
    return redirect("/")


def nova_empresa(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovaEmpresa(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                cnpj = request.POST.get("cnpj")
                nome_da_empresa = request.POST.get("nome_da_empresa")
                nome_do_responsavel = request.POST.get("nome_do_responsavel")
                slug_da_empresa = nome_da_empresa.replace(" ", "-")
                telefone = request.POST.get("telefone")

                usuario_administrador = request.POST.get("administrador")
                email = request.POST.get("email")
                senha = request.POST.get("senha")

                user = User.objects.create_user(
                    username=usuario_administrador,
                    email=email,
                    password=senha
                )

                emp = Empresa.objects.create(
                    cnpj=cnpj,
                    slug_da_empresa=slug_da_empresa,
                    nome_da_empresa=nome_da_empresa,
                    nome_do_responsavel=nome_do_responsavel,
                    telefone=telefone
                )

                login = Login.objects.create(
                    usuario=user,
                    empresa=emp,
                    nivel=Nivel.objects.get(id=1)
                )

                if emp:
                    cria_pasta(f"media/{slug_da_empresa}")
                return redirect("/administracao/")
        context = {"form": form}
        return render(request, "empresa/public/nova_empresa.html", context)
    return redirect("/")


def excluir_empresa(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(empresa=id)
        for login in logins:
            User.objects.get(username=login.usuario.username).delete()
        emp = Empresa.objects.get(id=id)
        shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.slug_da_empresa}",
                      ignore_errors=True)
        emp.delete()
        return redirect("/administracao/")
    return redirect("/")
