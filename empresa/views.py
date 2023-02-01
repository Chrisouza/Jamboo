from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants

from .models import Empresa

from .forms import FormNovaEmpresa

# Create your views here.
def minhas_empresas(request):
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(id_adm=request.user.pk)
        print(empresas)
        context = {
            'empresas':empresas
        }
        return render(request, 'empresa/public/empresas.html', context)
    return redirect("/account/login/")

def nova_empresa(request):
    if request.user.is_authenticated:
        form_empresa = FormNovaEmpresa(request.POST or None)
        if request.method == "POST":
            if form_empresa.is_valid():
                nome = request.POST.get('nome')
                slug = nome.replace(" ", "-")
                telefone = request.POST.get('telefone')
                save_emp = Empresa(id_adm=request.user.pk, slug=slug, nome=nome, telefone=telefone)
                save_emp.save()
                if save_emp.pk:
                    messages.add_message(request, constants.INFO, "Voce criou uma nova empresa para administrar")
                    return redirect("/empresa/minhas-empresas/")
                else:
                    messages.add_message(request, constants.WARNING, "ERRO CADASTRAR NOVA EMPRESA")
        context = {
            'form':form_empresa
        }
        return render(request, 'empresa/public/nova-empresa.html', context)
    return redirect("/account/login/")


def empresa(request, id):
    if request.user.is_authenticated:
        empresa = Empresa.objects.get(id_adm=request.user.pk, id=id)
        context = {
            'empresa':empresa
        }
        return render(request, 'empresa/public/empresa.html', context)
    return redirect("/account/login/")