from django.conf import settings

from django.shortcuts import render, redirect

from empresa.models import Empresa
from .models import Arquivo

from .forms import FormAdicionaArquivo


def upload_function(arquivo, slug, tipo, name):
    with open(f'{settings.BASE_DIR}/media/{slug}/{tipo}/{name}', 'wb+') as destination:
        for chunk in arquivo.chunks():
            destination.write(chunk)
    return f'/media/{slug}/{tipo}/{name}'

def index(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        empresa = Empresa.objects.get(id=id)
        arquivos = Arquivo.objects.filter(empresa_id=id)
        context = {
            'emp_id':id,
            'empresa':empresa,
            'arquivos':arquivos
        }
        return render(request, "arquivo/public/home.html", context)
    return redirect("/")

def novo_arquivo(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormAdicionaArquivo()
        if request.method == "POST":
            emp = Empresa.objects.get(id=id)
            arquivo = request.FILES.get('arquivo')
            slug = emp.slug
            tipo = arquivo.name.split(".")[-1]
            if tipo not in settings.FOLDERS:
                tipo = 'outros'
            name = arquivo.name.replace(" ", "_")
            path = upload_function(arquivo, slug, tipo, name)
            nome = request.POST.get('nome')
            Arquivo.objects.create(empresa_id=id, arquivo=path, nome=name, tipo=tipo)
            return redirect(f"/arquivos/{id}")
        context = {
            "emp_id":id,
            'form':form
        }
        return render(request, "arquivo/public/novo_arquivo.html", context)
    return redirect("/")
