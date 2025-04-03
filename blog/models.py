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
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="E-mail")
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name="Link | URL")

    prefeito = models.CharField(max_length=50)
    ano = models.ForeignKey(Ano, related_name='prefeituras', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class PastaAdministrativa(models.Model):
    prefeitura = models.ForeignKey(Prefeitura, related_name="prefeitura_related_pasta", null=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nome_filter = models.CharField(max_length=30)
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="E-mail")
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")

    facebook = models.URLField(max_length=255, null=True, blank=True, verbose_name="Facebook")
    instagram = models.URLField(max_length=255, null=True, blank=True, verbose_name="Instagram")
    twitter = models.URLField(max_length=255, null=True, blank=True, verbose_name="Twitter")
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name="LinkedIn")
    youtube = models.URLField(max_length=255, null=True, blank=True, verbose_name="YouTube")

    def __str__(self):
        return self.nome



    def __str__(self):
        return self.nome


class Secretario(models.Model):
    nome = models.CharField(max_length=100)
    pasta = models.ForeignKey(PastaAdministrativa, related_name='pastaAdministrativa_related', on_delete=models.CASCADE)
    prefeitura = models.ForeignKey(Prefeitura, related_name='secretarios', on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="E-mail")
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")

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
    
    # Limita o número de registros no model
    def save (self, *args, **kwargs):
        limite = 10
        if not self.pk and TipoPublicacao.objects.count() >= limite:
            raise ValueError(f'Limite de {limite} tópicos atingido.')
        super().save(*args, **kwargs)


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

    class Meta:
        ordering = ['-data_publicacao']

    def curtidas_count(self):
        return self.curtidas.count()
    
    def __str__(self):
        return self.titulo


class Curtida(models.Model):
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name='curtidas')
    data_curtida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} curtiu {self.publicacao.titulo}'
                                                                                           

class Comentarios(models.Model):
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name='comentarios')
    data_coment = models.DateTimeField(auto_now_add=True)    
    comentario = RichTextUploadingField()  # Usando o CKEditor para texto rico    

    def __str__(self):
        return f' {self.comentario}'
    
    
class ViewsPost(models.Model):
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')
    publicacao = models.ForeignKey(Publicacao, null=True, on_delete=models.CASCADE, related_name='visualiza')
    data_view = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'visualizações {self.publicacao}'
    
# -------------------- Escolas --------------------------
# -------------------------------------------------------

from django.db import models
from django.core.exceptions import ValidationError

class Escola(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

class ProjetoPoliticoPedagogico(models.Model):
    escola = models.OneToOneField(Escola, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_criacao = models.DateField(auto_now_add=True)
    data_atualizacao = models.DateField(auto_now=True)
    documento = models.FileField(upload_to='ppp_documentos/', blank=True, null=True)
    
    def clean(self):
        # Garante que apenas um PPP por escola seja registrado
        if ProjetoPoliticoPedagogico.objects.filter(escola=self.escola).exclude(id=self.id).exists():
            raise ValidationError('Esta escola já possui um Projeto Político Pedagógico registrado.')

    def __str__(self):
        return f"PPP de {self.escola.nome}"
    
    

# ----------------- CONSELHOS ---------------------------------
# -------------------------------------------------------------
from django.db import models

class Conselho(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class MembroConselho(models.Model):
    conselho = models.ForeignKey(Conselho, on_delete=models.CASCADE, related_name='membros')
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cargo} ({self.conselho.nome})"

class ReuniaoConselho(models.Model):
    conselho = models.ForeignKey(Conselho, on_delete=models.CASCADE, related_name='reunioes')
    data = models.DateField()
    pauta = models.TextField()
    ata = models.FileField(upload_to='atas_conselho/', blank=True, null=True)

    def __str__(self):
        return f"Reunião de {self.conselho.nome} - {self.data}"
    



# Pos MIGRATS -------------------------------------------------
@receiver(post_migrate)
def criar_registros_exemplo(sender, **kwargs):
    # Verifica se o ano 2025 já existe, se não, cria
    if not Ano.objects.exists():
        ano_2025, created = Ano.objects.get_or_create(ano=2025)    

    if not Prefeitura.objects.exists():
        # Cria a prefeitura se não existir
        ano = Ano.objects.get(id=1)
        prefeitura, created = Prefeitura.objects.get_or_create(
            nome="Prefeitura Municipal de Exemplo", prefeito="Igor Pinho", ano=ano
        )
    if not PastaAdministrativa.objects.exists():
        # Cria pasta administrativa
        pastaAdministrativa, created = PastaAdministrativa.objects.get_or_create(
            prefeitura = Prefeitura.objects.get(nome="Prefeitura Municipal de Exemplo"),
            nome = "Secretaria Municipal da Educação Educação",
            nome_filter = "educação"
        )
    if not Secretario.objects.exists():
        # Cria o secretário se não existir
        secretario, created = Secretario.objects.get_or_create(
            nome="Silvano Sulzart",
            pasta=PastaAdministrativa.objects.get(id = 1),
            prefeitura=Prefeitura.objects.get(id=1),
            data_inicio="2025-01-01"
        )
    if not TipoPublicacao.objects.exists():
        # Adiciona uma publicação de exemplo
        tipo_publicacao, created = TipoPublicacao.objects.get_or_create(nome="Edital")
        Publicacao.objects.get_or_create(
            titulo="Exemplo de Publicação",
            descricao="<p>Esta é uma publicação de exemplo criada automaticamente após a migração.</p>",
            data_publicacao="2025-02-06",
            tipo_publicacao=tipo_publicacao,
            secretario=secretario
        )

