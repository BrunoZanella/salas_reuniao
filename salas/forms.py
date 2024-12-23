from django import forms
from .models import Sala

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nome', 'imagem', 'tamanho', 'capacidade']
