from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from  blog.models import Publicacao
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

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
            return redirect(reverse_lazy('painel:publicacao_create'))
        else:
            messages.error(request, "Credenciais inválidas. Por favor, verifique seu usuário e senha.")
            return redirect(reverse_lazy('blog:home'))
    
    return redirect(reverse_lazy('blog:home'))






# Publicações ******************************************************************
class PublicacaoListView(ListView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_list.html'
    context_object_name = 'publicacoes'
    paginate_by = 10  # Se quiser paginação

class PublicacaoCreateView(CreateView):
    model = Publicacao
    template_name = 'publicar/creater_publica.html'
    fields = ['titulo', 'descricao',  'tipo_publicacao',  'em_destaque', 'imagem', 'video']
    success_url = reverse_lazy('publicacoes:publicacao_list')  # Redireciona para a lista após criar

class PublicacaoUpdateView(UpdateView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_form.html'
    fields = ['titulo', 'descricao', 'data_publicacao', 'tipo_publicacao', 'secretario', 'em_destaque', 'imagem', 'video']
    success_url = reverse_lazy('publicacoes:publicacao_list')  # Redireciona para a lista após editar

class PublicacaoDeleteView(DeleteView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_confirm_delete.html'
    success_url = reverse_lazy('publicacoes:publicacao_list')  # Redireciona para a lista após excluir

