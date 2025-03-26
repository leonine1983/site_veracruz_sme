from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.storage import default_storage

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

    # Garantir que o arquivo de imagem seja excluído quando o registro for deletado
    def delete(self, *args, **kwargs):
        """
        Exclui o objeto Link do banco de dados e remove o arquivo de imagem
        associado do armazenamento.

        Antes de deletar do banco de dados, este método verifica se há um arquivo de
        imagem associado ao campo 'icone' e o remove do sistema de arquivos caso ele exista.

        Uso: 
            link = Link.objects.get(id=1)
            link.delete()
        """
        if self.icone:
            if default_storage.exists(self.icone.name):
                default_storage.delete(self.icone.name)
        super().delete(*args, **kwargs)
