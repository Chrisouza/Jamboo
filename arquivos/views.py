from django.shortcuts import render
from django.shortcuts import redirect
from .models import Arquivo
from .forms import FormArquivo

def index(request):
    if not request.user.is_authenticated:
        return redirect("/usuarios/login")
    files = Arquivo.objects.all()
    context = {
        'files':files
    }
    return render(request, 'arquivos/public/home.html', context)

def add_file(request):
    if not request.user.is_authenticated:
        return redirect("/usuarios/login")
    form = FormArquivo(request.POST or None)
    context = {
        'form':form
    }
    return render(request, 'arquivos/public/add.html', context)