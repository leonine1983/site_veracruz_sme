from  blog.models import Publicacao
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
    fields = ['titulo', 'descricao',  'tipo_publicacao', 'secretario', 'imagem', 'video']
    success_url = reverse_lazy('painel:publicacao_list')

    def form_valid(self, form):
        if self.request.user.first_name:
            author = f'{self.request.user.first_name} {self.request.user.last_name}'
        else:
            author = self.request.user

        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
        form.save(commit=False)
        form.instance.author = author
        form.save()
        return super().form_valid(form)

# Edição de publicação
class PublicacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_form.html'
    fields = ['titulo', 'descricao', 'data_publicacao', 'tipo_publicacao', 'secretario', 'imagem', 'video']
    success_url = reverse_lazy('publicacao_list')

# Exclusão de publicação
class PublicacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_confirm_delete.html'
    success_url = reverse_lazy('publicacao_list')

