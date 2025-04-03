from  blog.models import TipoPublicacao, Publicacao, Prefeitura, Secretario
from .models import Link
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from dashboard.forms import *


def loginCreated(request):    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")        
        user = authenticate(request, username=username, password=password)
        print (f'esse é o login {user}')
        
        if user is not None:
            # Enviar email
            """
            subject = 'Login realizado com sucesso'
            message = f'Olá {user.username}, você fez login com sucesso no painel.'
            recipient_list = [user.email]  # Lista de destinatários (usuário logado)            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            """
            login(request, user)            
            messages.success(request, "Login realizado com sucesso. Bem-vindo ao painel!")
            return redirect(reverse_lazy('painel:publicacao_list'))
        else:
            messages.error(request, "Credenciais inválidas. Por favor, verifique seu usuário e senha.")
            return redirect(reverse_lazy('blog:home'))
    
    return redirect(reverse_lazy('blog:home'))

def user_logout(request):
    # Realiza o logout do usuário
    messages.success(request, '<i class="fas fa-exclamation-circle"></i> Você não está mais logado. Para realizar publicações, é necessário fazer login novamente.')
    logout(request)
    # Redireciona para a página inicial ou qualquer outra página
    return redirect(reverse_lazy('blog:home'))


# Listagem de publicações
class PublicacaoListView(LoginRequiredMixin, ListView):
    model = Publicacao
    template_name = 'publicar/list_publica.html'
    context_object_name = 'publicacoes'
    paginate_by = 10  # Número de publicações por página

    def get_queryset(self):
        return Publicacao.objects.all().order_by('-data_publicacao')

# Detalhes de uma publicação
class PublicacaoDetailView(LoginRequiredMixin, DetailView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_detail.html'
    context_object_name = 'publicacao'

# Criação de publicação
class PublicacaoCreateView(LoginRequiredMixin, CreateView):
    model = Publicacao
    template_name = 'publicar/creater_publica.html'
    fields = ['titulo', 'descricao','em_destaque','em_urgentes','ocultar_titulo_carrocel', 'tipo_publicacao', 'secretario', 'imagem', 'video']
    success_url = reverse_lazy('painel:publicacao_list')

    def form_valid(self, form):
        if self.request.user.first_name:
            author = f'{self.request.user.first_name} {self.request.user.last_name}'
        else:
            author = f'{self.request.user}'

        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
        form.save(commit=False)
        form.instance.author = author
        form.save()
        return super().form_valid(form)
    

# Edição de publicação
class PublicacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Publicacao
    template_name = 'publicar/creater_publica.html'
    fields = ['titulo', 'descricao', 'tipo_publicacao', 'secretario', 'imagem', 'video']
    success_url = reverse_lazy('painel:publicacao_list')

    def form_valid(self, form):
        if self.request.user.first_name:
            author = f'{self.request.user.first_name} {self.request.user.last_name}'
        else:
            author = f'{self.request.user}'

        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
        form.save(commit=False)
        form.instance.author = author
        form.save()
        return super().form_valid(form)
    

#PREFEITURA ------------------------------------------------
# list de prefeitura
class  ListPrefeituraView(LoginRequiredMixin, ListView):
    model = Prefeitura
    template_name = 'prefeitura/prefeitura_edit.html'  
    

# Edição de prefeitura
class EditaPrefeituraView(LoginRequiredMixin, UpdateView):
    model = Prefeitura
    template_name = 'prefeitura/prefeitura_edit.html'
    fields = ['nome', 'email', 'endereco', 'telefone', 'prefeito', 'link ']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Prefeitura.objects.all()
        context['edit'] = True
        return context

    def form_valid(self, form):
        if self.request.user.first_name:
            author = f'{self.request.user.first_name} {self.request.user.last_name}'
        else:
            author = f'{self.request.user}'

        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
        form.save(commit=False)
        form.instance.author = author
        form.save()

        # Adiciona uma mensagem de sucesso
        messages.success(self.request, "Prefeitura atualizada com sucesso!")

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('painel:Prefeitura_edit', kwargs = {'pk': self.get_object().pk})
    

# SECRETARIA ------------------------------------------------
# list de secretaria
class  ListSecretarioView(LoginRequiredMixin, ListView):
    model = Secretario
    template_name = 'secretaria/secretaria_edit.html'  
    

# Edição de prefeitura
class EditaSecretarioView(LoginRequiredMixin, UpdateView):
    model = Secretario
    template_name = 'secretaria/secretaria_edit.html'  
    fields = ['nome', 'pasta', 'email', 'endereco', 'telefone', 'ativo']    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Secretario.objects.all()
        context['edit'] = True
        return context

    def form_valid(self, form):
        if self.request.user.first_name:
            author = f'{self.request.user.first_name} {self.request.user.last_name}'
        else:
            author = f'{self.request.user}'

        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
        form.save(commit=False)
        form.instance.author = author
        form.save()

        # Adiciona uma mensagem de sucesso
        messages.success(self.request, "Informações da Secretaria atualizada com sucesso!")

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('painel:Secretaria_edit', kwargs = {'pk': self.get_object().pk})
    

    

# Exclusão de publicação
class PublicacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_confirm_delete.html'
    success_url = reverse_lazy('publicacao_list')



# Views para a criação de links --------------------------------

class LinkListView(LoginRequiredMixin, ListView):
    model = Link
    template_name = 'links/link_list.html'
    context_object_name = 'links'

class LinkDetailView(DetailView):
    model = Link
    template_name = 'links/link_detail.html'
    context_object_name = 'link'

class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    template_name = 'links/creater_links.html'
    fields = ['nome', 'url', 'icone', 'descricao', 'painel']
    success_url = reverse_lazy('painel:link_list')

class LinkUpdateView(UpdateView):
    model = Link
    template_name = 'links/link_form.html'
    fields = ['nome', 'url', 'icone', 'descricao']
    success_url = reverse_lazy('link_list')





from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Link

class LinkDeleteView(View):
    def post(self, request, *args, **kwargs):
        link = get_object_or_404(Link, pk=kwargs['pk'])
        link.delete()
        
        # Adiciona a mensagem de sucesso
        messages.success(request, "Link excluído com sucesso.")
        
        # Redireciona de volta para a página de links
        return redirect(reverse_lazy('blog:home'))  # Altere 'link_list' para o nome correto da sua URL
    
    
class LinkDeleteViewPainel(LoginRequiredMixin, DeleteView):
    model = Link
    template_name = 'links/creater_links.html'
    success_url = reverse_lazy('painel:link_list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto"] = f"Tem certeza de que deseja excluir o link '{self.object}'?"
        context["bottom"] = "Confirmar exclusão"
        return context
    

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"O link '{self.object}' foi excluído com sucesso.")
        return response
    

# Views de criação de TIPOS DE PUBLICAÇÃO
class TiposPublicacaoCreateView(LoginRequiredMixin, CreateView):
    model = TipoPublicacao
    template_name = 'tipos_publica/creater_tiposPublica.html'
    fields = ['nome', 'svg']

    success_url = reverse_lazy('painel:publicacao_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['category'] = TipoPublicacao.objects.all()
        return context

    

