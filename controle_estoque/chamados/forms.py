from django import forms
from .models import Chamado

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['nome', 'sobrenome', 'whatsapp', 'email', 'ramal', 'numero_anydesk', 'departamento', 'tipo_problema', 'descricao_problema', 'urgencia']
        widgets = {
            'descricao_problema': forms.Textarea(attrs={'rows': 4}),
        }
