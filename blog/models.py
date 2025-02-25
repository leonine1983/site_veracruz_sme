from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import timezone
from django.contrib.auth.models import User

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

class PastaAdministrativa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Secretario(models.Model):
    nome = models.CharField(max_length=100)
    pasta = models.ForeignKey(PastaAdministrativa, related_name='pastaAdministrativa_related', on_delete=models.CASCADE)
    prefeitura = models.ForeignKey(Prefeitura, related_name='secretarios', on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class TipoPublicacao(models.Model):
    nome = models.CharField(max_length=100)
    svg = models.CharField(max_length=100, verbose_name="Adicionar TAG <i> do fontawesome")
    
    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    author = models.CharField(max_length=100, blank=True, null=True) 
    titulo = models.CharField(max_length=100)    
    descricao = RichTextUploadingField()  # Usando o CKEditor para texto rico
    data_publicacao = models.DateField(auto_now=True)
    data_atualiza = models.DateField(auto_now_add=True)
    tipo_publicacao = models.ForeignKey(TipoPublicacao, related_name='publicacoes', on_delete=models.CASCADE)
    secretario = models.ForeignKey(Secretario, related_name='publicacoes', on_delete=models.CASCADE, verbose_name="Selecione o nome do secretário atualmente em exercício.")
    em_destaque = models.BooleanField(default=False, verbose_name="Deseja por em destaque a publicação? Isso irá substituir a última publicação em destaque")
    em_urgentes = models.BooleanField(default=False, verbose_name="Selecione esta opção se deseja marcar como urgente ou de última hora.")
    ocultar_titulo_carrocel = models.BooleanField(default=False, verbose_name="Selecione a opção ao publicar imagens com texto para evitar sobreposição. Isso assegura uma apresentação visual mais limpa e facilita a compreensão da informação no carrossel.")
    
    # Campos adicionais para imagens e vídeos
    imagem = models.ImageField(upload_to='publicacoes/imagens/', null=True, blank=True)
    video = models.FileField(upload_to='publicacoes/videos/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo


# Função para registrar exemplo de Prefeitura e Secretário
@receiver(post_migrate)
def criar_registros_exemplo(sender, **kwargs):
    # Verifica se o ano 2025 já existe, se não, cria
    if not Ano.objects.exists:
        ano_2025, created = Ano.objects.get_or_create(ano=2025)    

    if not Prefeitura.objects.exists:
        # Cria a prefeitura se não existir
        prefeitura, created = Prefeitura.objects.get_or_create(
            nome="Prefeitura Municipal de Exemplo", prefeito="Igor Pinho", ano=ano_2025
        )
    if not PastaAdministrativa.objects.exists:
        # Cria pasta administrativa
        pastaAdministrativa, created = PastaAdministrativa.objects.get_or_create(
            nome = "Educação"
        )
    if not Secretario.objects.exists:
        # Cria o secretário se não existir
        secretario, created = Secretario.objects.get_or_create(
            nome="Silvano Sulzart",
            pasta=PastaAdministrativa.objects.get(nome = "Educação"),
            prefeitura=prefeitura,
            data_inicio="2025-01-01"
        )
    if not TipoPublicacao.objects.exists:
        # Adiciona uma publicação de exemplo
        tipo_publicacao, created = TipoPublicacao.objects.get_or_create(nome="Edital")
        Publicacao.objects.get_or_create(
            titulo="Exemplo de Publicação",
            descricao="<p>Esta é uma publicação de exemplo criada automaticamente após a migração.</p>",
            data_publicacao="2025-02-06",
            tipo_publicacao=tipo_publicacao,
            secretario=secretario
        )

