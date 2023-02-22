from django import forms
from .models import Company


class FormNewCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        exclude = ["slug", "created", "active"]
