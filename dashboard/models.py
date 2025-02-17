from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Link(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Site')
    url = models.URLField(verbose_name='URL do Site')
    icone = models.ImageField(upload_to='icones/', null=True, blank=True, verbose_name='Ícone (PNG)')
    descricao = RichTextUploadingField()
    painel = models.BooleanField(default=False, verbose_name='Gostaria de adicionar este link ao painel de links? Caso não selecione esta opção, o link será exibido apenas no rodapé do site.')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
