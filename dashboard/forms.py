from django.forms import forms
from blog.models import Publicacao

class CreatePublic_form (forms.Form):
    class Meta:
        fields = ['tipo_publicacao','titulo', 'descricao', 'destaque', 'imagem', 'video']

    pass

"""
class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = RichTextUploadingField()  # Usando o CKEditor para texto rico
    data_publicacao = models.DateField()
    tipo_publicacao = models.ForeignKey(TipoPublicacao, related_name='publicacoes', on_delete=models.CASCADE)
    secretario = models.ForeignKey(Secretario, related_name='publicacoes', on_delete=models.CASCADE)
    em_destaque = models.BooleanField(default=False, verbose_name="Deseja por em destaque a publicação? Isso irá substituir a última publicação em destaque")
    
    # Campos adicionais para imagens e vídeos
    imagem = models.ImageField(upload_to='publicacoes/imagens/', null=True, blank=True)
    video = models.FileField(upload_to='publicacoes/videos/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo

"""