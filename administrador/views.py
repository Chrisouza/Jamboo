from django.shortcuts import render
from .models import Administrador
from .forms import FormNovoAdm
from django.shortcuts import redirect

def novo_adm(request):
    form = FormNovoAdm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            adm = Administrador()
            adm.nome = request.POST.get('nome')
            adm.email = request.POST.get('email')
            adm.senha = adm.make_password( password=request.POST.get('senha') )
            adm.save()
            return redirect("/mensagem/admin-cadastrado")
    context = {
        'form':form
    }
    return render(request, "adm/public/novo.html", context)