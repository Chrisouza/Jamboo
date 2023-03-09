from django.shortcuts import render, redirect
from empresa.models import Company
from .models import File
from administracao.models import Login
from .forms import FormNewFile
from .funcoes import apaga_arquivo, verifica_tipo_de_arquivo, read_files, upload_function


def index(request, id):
    if request.user.is_authenticated:
        try:
            level = Login.objects.get(user=request.user.pk)
        except:
            print("NAO CONSEGUIU ENCONTRAR O USUARIO LOGADO")
            return False
        empresa = Company.objects.get(id=id)
        arquivos = read_files(slug=empresa.slug)
        context = {
            "emp_id": id,
            "empresa": empresa,
            "arquivos": arquivos,
            "level": level.level.level,
        }
        return render(request, "arquivo/public/home.html", context)
    return redirect("/")


def novo_arquivo(request, id):
    if request.user.is_authenticated:
        form = FormNewFile()
        if request.method == "POST":
            emp = Company.objects.get(id=id)
            arquivo = request.FILES.get("file")
            slug = emp.slug
            tipo = arquivo.name.split(".")[-1]
            tipo = verifica_tipo_de_arquivo(tipo)
            path = upload_function(arquivo, slug, tipo)
            File.objects.create(
                company=emp,
                file=path,
                editor=request.user
            )
            return redirect(f"/arquivos/{id}/")
        context = {"emp_id": id, "form": form}
        return render(request, "arquivo/public/novo_arquivo.html", context)
    return redirect("/")


def excluir_arquivo(request, id_emp, nome_arquivo):
    if request.user.is_authenticated:
        level = Login.objects.get(user=request.user)
        print(level.level)
        emp = Company.objects.get(id=id_emp)
        arq = File.objects.filter(
            file__contains=nome_arquivo,
            company=id_emp
        )
        if arq is not None:
            apaga_arquivo(path=f"media/{emp.slug}/audios/{nome_arquivo}")
            arq.delete()
    return redirect(f"/arquivos/{id_emp}/")
