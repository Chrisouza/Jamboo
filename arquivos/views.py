from django.shortcuts import render, redirect
from empresa.models import Empresa, Arquivo
from .forms import FormNovoArquivo
from .funcoes import apaga_arquivo, verifica_tipo_de_arquivo, upload_function


def index(request, id):
    if request.user.is_authenticated:
        empresa = Empresa.objects.get(id=id)
        # arquivos = read_files(slug=empresa.slug)
        arquivos = Arquivo.objects.filter(company=id).order_by('type')
        context = {
            "emp_id": id,
            "empresa": empresa,
            "arquivos": arquivos
        }
        return render(request, "arquivo/public/home.html", context)
    return redirect("/")


def novo_arquivo(request, id):
    if request.user.is_authenticated:
        form = FormNovoArquivo()
        if request.method == "POST":
            emp = Empresa.objects.get(id=id)
            arquivo = request.FILES.get("file")
            slug = emp.slug
            tipo = arquivo.name.split(".")[-1]
            tipo = verifica_tipo_de_arquivo(tipo)
            path = upload_function(arquivo, slug, tipo)
            Arquivo.objects.create(
                company=emp,
                file=path,
                editor=request.user,
                type=tipo
            )
            return redirect(f"/arquivos/{id}/")
        context = {"emp_id": id, "form": form}
        return render(request, "arquivo/public/novo_arquivo.html", context)
    return redirect("/")


def excluir_arquivo(request, id_emp, nome_arquivo):
    if request.user.is_authenticated:
        emp = Empresa.objects.get(id=id_emp)
        arq = Arquivo.objects.filter(
            file__contains=nome_arquivo,
            company=id_emp
        )
        slug = arq[0].file.split("/")[-2]
        if arq is not None:
            apaga_arquivo(path=f"media/{emp.slug}/{slug}/{nome_arquivo}")
            arq.delete()
    return redirect(f"/arquivos/{id_emp}/")
