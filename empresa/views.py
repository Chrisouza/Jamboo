import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from administracao.models import Login
from .models import Empresa
from django.contrib.auth.models import User
from .forms import FormNovaEmpresa
from .funcoes import cria_pasta

def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        empresa = Empresa.objects.get(id=Login.objects.get(user=request.user).empresa.id)
        context = { "empresa": empresa }
        return render(request, "empresa/public/home.html", context)
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
                    cria_pasta(f"media/{slug}")
                    for folder in settings.FOLDERS:
                        cria_pasta(f"media/{slug}/{folder}")
                return redirect("/administracao/")
        context = { "form":form }
        return render(request, "empresa/public/nova_empresa.html", context)
    return redirect("/")

def excluir_empresa(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(empresa=id)
        for login in logins:
            User.objects.get(id=login.user_id).delete()
            login.delete()
        emp = Empresa.objects.get(id=id).delete()
        shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.slug}", ignore_errors=True)
        return redirect("/administracao/")
    return redirect("/")
