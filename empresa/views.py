from django.shortcuts import render, redirect
from administracao.models import Empresa, Login

def index(request):
    if request.user.is_authenticated:
        my_enterprise = Login.objects.get(user_id=request.user.pk)
        print(my_enterprise.enterprise)
        context = {
            "enterprise": my_enterprise
        }
        return render(request, 'empresa/public/home.html', context)
    redirect("/")
