from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from .forms import FormRegistre, FormLogin

from django.contrib.auth.models import User
from empresa.models import Empresa

# Create your views here.
def index(request):
    context = {}
    return render(request, 'account/public/home.html', context)

def registre(request):
    form_registre = FormRegistre(request.POST or None)
    if request.method == "POST":
        if form_registre.is_valid():
            empresa = request.POST.get('empresa')
            ver_emp = Empresa.objects.filter(nome=empresa)
            print(ver_emp.count())
            if not ver_emp:
                nome = request.POST.get('nome')
                email = request.POST.get('email')
                senha = request.POST.get('senha')
                user = User.objects.create_user(username=nome, email=email, password=senha)
                emp = Empresa(adm_id=user.pk, nome=empresa)
                emp.save()
                
                messages.add_message(request, messages.INFO, 'Dados cadastrados com sucesso.')

                return redirect('/account/')
            else:
                messages.add_message(request, messages.INFO, 'Essa empresa ja esta cadastrada.')
                form_registre = FormRegistre(request.POST or None)
    context = {
        'form':form_registre
    }
    return render(request, 'account/public/registre.html', context)

def logar(request):
    form_logar = FormLogin(request.POST or None)
    context = {
        'form':form_logar
    }
    return render(request, 'account/public/registre.html', context)