from django.contrib import admin
from empresa.models import Arquivo, Backups, Empresa, Nivel, Login, Notificacoes, Projeto, Tarefas, TipoEvento


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ["cnpj", "slug_da_empresa", "nome_da_empresa",
                    "nome_do_responsavel", "telefone", "pasta", "criado", "ativo"]


admin.site.register(Empresa, EmpresaAdmin)


class NivelAdmin(admin.ModelAdmin):
    list_display = ["nome_do_nivel", "descricao", "data_criado"]


admin.site.register(Nivel, NivelAdmin)


class LoginAdmin(admin.ModelAdmin):
    list_display = ["usuario", "empresa",
                    "nivel", "primeiro_acesso", "data_criado"]


admin.site.register(Login, LoginAdmin)


class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ['nome']


admin.site.register(TipoEvento, TipoEventoAdmin)


class TarefasAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'titulo', 'descricao', 'inicio_data',
                    'inicio_hora', 'fim_data', 'fim_hora', 'tipo', 'data']


admin.site.register(Tarefas, TarefasAdmin)


class NotificacoesAdmin(admin.ModelAdmin):
    list_display = ["descricao", 'empresa', 'visto', 'data']


admin.site.register(Notificacoes, NotificacoesAdmin)
# ###########################3


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['slug_do_projeto',
                    'nome_do_projeto', 'empresa', 'data_criado']


admin.site.register(Projeto, ProjetoAdmin)


class ArquivoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'file', 'descricao', 'editor',
                    'edicao', 'extensao', 'projeto', 'data_upload']


admin.site.register(Arquivo, ArquivoAdmin)


class BackupsAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'usuario', 'projeto', 'data']


admin.site.register(Backups, BackupsAdmin)
