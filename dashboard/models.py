from django.db import models

class Link(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Site')
    url = models.URLField(verbose_name='URL do Site')
    icone = models.ImageField(upload_to='icones/', null=True, blank=True, verbose_name='Ícone (PNG)')
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição do Site')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
