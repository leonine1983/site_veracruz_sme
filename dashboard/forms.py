from django import forms
from blog.models import Publicacao, Secretario

class CreatePublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['tipo_publicacao', 'titulo', 'descricao', 'em_destaque', 'imagem', 'video', 'secretario', 'ocultar_titulo_carrocel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['secretario'].queryset = Secretario.objects.filter(ativo=True)

