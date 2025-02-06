from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Ano(models.Model):
    ano = models.PositiveIntegerField(unique=True)
    
    def __str__(self):
        return str(self.ano)

class Prefeitura(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.ForeignKey(Ano, related_name='prefeituras', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Secretario(models.Model):
    nome = models.CharField(max_length=100)
    prefeitura = models.ForeignKey(Prefeitura, related_name='secretarios', on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.nome

class TipoPublicacao(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = RichTextUploadingField()  # Usando o CKEditor para texto rico
    data_publicacao = models.DateField()
    tipo_publicacao = models.ForeignKey(TipoPublicacao, related_name='publicacoes', on_delete=models.CASCADE)
    secretario = models.ForeignKey(Secretario, related_name='publicacoes', on_delete=models.CASCADE)
    
    # Campos adicionais para imagens e vídeos
    imagem = models.ImageField(upload_to='publicacoes/imagens/', null=True, blank=True)
    video = models.FileField(upload_to='publicacoes/videos/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo
