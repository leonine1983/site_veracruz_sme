from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Ano(models.Model):
    ano = models.PositiveIntegerField(unique=True)
    
    def __str__(self):
        return str(self.ano)

class Prefeitura(models.Model):
    nome = models.CharField(max_length=100)
    prefeito = models.CharField(max_length=50)
    ano = models.ForeignKey(Ano, related_name='prefeituras', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Secretario(models.Model):
    nome = models.CharField(max_length=100)
    pasta = models.CharField(max_length=100)
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


# Função para registrar exemplo de Prefeitura e Secretário
@receiver(post_migrate)
def criar_registros_exemplo(sender, **kwargs):
    # Verifica se o ano 2025 já existe, se não, cria
    ano_2025, created = Ano.objects.get_or_create(ano=2025)

    # Cria a prefeitura se não existir
    prefeitura, created = Prefeitura.objects.get_or_create(
        nome="Prefeitura Municipal de Exemplo", prefeito="Igor Pinho", ano=ano_2025
    )

    # Cria o secretário se não existir
    secretario, created = Secretario.objects.get_or_create(
        nome="Silvano Sulzart",
        pasta="Secretaria de Educação",
        prefeitura=prefeitura,
        data_inicio="2025-01-01"
    )

    # Adiciona uma publicação de exemplo
    tipo_publicacao, created = TipoPublicacao.objects.get_or_create(nome="Edital")
    Publicacao.objects.get_or_create(
        titulo="Exemplo de Publicação",
        descricao="<p>Esta é uma publicação de exemplo criada automaticamente após a migração.</p>",
        data_publicacao="2025-02-06",
        tipo_publicacao=tipo_publicacao,
        secretario=secretario
    )

