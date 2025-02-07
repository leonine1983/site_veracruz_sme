from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Publicacao
from django.contrib.auth.mixins import LoginRequiredMixin

def blog(request):
    context = Publicacao.objects.all()
    return render(request, 'index.html', {'context': context})



# Listagem de publicações
class PublicacaoListView(LoginRequiredMixin, ListView):
    model = Publicacao
    template_name = 'publicacoes/publicacao_list.html'
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
    template_name = 'publicacoes/publicacao_form.html'
    fields = ['titulo', 'descricao', 'data_publicacao', 'tipo_publicacao', 'secretario', 'imagem', 'video']
    success_url = reverse_lazy('publicacao_list')

    def form_valid(self, form):
        # Você pode adicionar lógica adicional para salvar o formulário ou fazer algo antes de salvar
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

