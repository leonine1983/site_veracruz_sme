from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from  blog.models import Publicacao
from django.urls import reverse_lazy

class LoginSme(LoginView):
    template_name = 'login.html'    

    def get_success_url(self):
        return reverse_lazy('painel:dashboard')  # Redireciona para o dashboard



class Painel(TemplateView):
    template_name = 'dashboard.html'


# Publicações ******************************************************************
class PublicacaoListView(ListView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_list.html'
    context_object_name = 'publicacoes'
    paginate_by = 10  # Se quiser paginação

class PublicacaoCreateView(CreateView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_form.html'
    fields = ['titulo', 'descricao', 'data_publicacao', 'tipo_publicacao', 'secretario', 'em_destaque', 'imagem', 'video']
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

