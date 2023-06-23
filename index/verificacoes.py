from empresa.models import Login, Empresa
from index.mensagens import info

# VERIFICACOES DE USUARIO


def permissoes(request, empresa):
    erros = 0
    try:
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(slug_da_empresa=empresa)
        if usuario.nivel.id != 1:
            erros += 1
        if usuario.empresa.id != empresa.id:
            erros += 1
    except:
        pass

    if erros > 0:
        info(request, msg="Você não tem permissão para acessar essa página!")
        return False
    return True
