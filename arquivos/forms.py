from django import forms

class FormAdicionaArquivo(forms.Form):
    arquivo = forms.FileField()
    nome = forms.CharField()