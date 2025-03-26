from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Publicacao, PastaAdministrativa, Secretario, ViewsPost, Curtida, Comentarios, TipoPublicacao
from dashboard.models import Link
from django.contrib import messages
from .models import Publicacao, Curtida
from django.db.models import Q
from django.core.paginator import Paginator  
from django.db.models import Count



def blog(request):
    secretario = Secretario.objects.all()

    
    if 'secretario' in request.GET:
        request.session.flush()
        id = request.GET['secretario']
        secretario = Secretario.objects.filter(id=id)
        request.session['secretario'] = secretario
        publica = Publicacao.objects.filter(secretario__id = id)
        ativo = True
    
    elif 'pesquisa' in request.GET:
        nome = request.GET['pesquisa']
        publica = Publicacao.objects.filter(Q(author__icontains = nome) | 
                                            Q(titulo__icontains = nome) | 
                                            Q(descricao__icontains = nome) | 
                                            Q(secretario__nome__icontains = nome) )
        ativo = 'busca'

    else:        
        request.session['secretario'] = secretario
        publica = Publicacao.objects.filter(secretario__ativo=True).annotate(num_curtidas=Count('curtidas')).order_by('-num_curtidas')
        publicacao = Publicacao.objects.filter(secretario__ativo = True)
        ativo = False

 
    paginator = Paginator(publica, 2)  # 10 publicações por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Obtém as publicações da página solicitada

    context = publica  # Use o objeto de página como contexto
    destaques = Publicacao.objects.filter(em_destaque=True).order_by('-data_publicacao', '-data_atualiza')[:4]


    links = Link.objects.all()    
    footer = PastaAdministrativa.objects.get(nome_filter = "educação")    
    nav = TipoPublicacao.objects.all()
    request.session['links'] = links
    request.session['publica'] = context
    request.session['footer'] = footer
    request.session['nav'] = nav
    colors = [
    # Tons suaves de verde
    #"#e6f7e6", "#d4f5d4", "#c2f0c2", "#b0eab0", "#9fe59f", "#8fdf8f",
    
    # Tons suaves de #c58233 (laranja queimado)
    "#eec9a5", "#e5b88a", "#d9a16d", "#c88a52", "#b97a45",

    # Tons suaves de #4c70aa (azul médio)
    "#d1d9eb", "#b7c6e0", "#9db3d5", "#839fc9", "#698bbe",

    # Tons suaves de #105f42 (verde escuro)
    "#a8d5c0", "#92c8b0", "#7cba9f", "#66ad8f", "#509f7f"
    # Tons suaves de cinza
    "#f2f2f2", "#e6e6e6", "#d9d9d9", "#cccccc", "#bfbfbf", "#b3b3b3"
    ]

    return render(request, 'index.html', {
        'page_obj':page_obj,
        'destaques':destaques,
        'ativo' : ativo,
        'context': context,
        'links': links,
        "colors": colors})


from django import forms
class ComentariosForm(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['comentario']  # Definindo quais campos do modelo aparecerão no formulário    



def visualizaPost(request, pk):
    post = Publicacao.objects.get(pk = pk)
    #Criar a visualização da postagem
    ViewsPost.objects.create(publicacao = post)    
    form = ComentariosForm()   
    
    return render(request, 'visualizaPost.html', {
        'post':post,
        'form': form,
        'tela_unica':True,
        })

def visualizaTipos(request, pk):
    post = Publicacao.objects.filter(tipo_publicacao__id = pk)
    #Criar a visualização da postagem
    #ViewsPost.objects.create(publicacao = post)  
    secretario_ativo = Secretario.objects.filter(ativo = True)  
    request.session['secretario'] = secretario_ativo

    form = ComentariosForm()   
    
    return render(request, 'visualizaTipos.html', {
        'post':post,
        'ativo':'true'
        })
 


def curtidaPost(request, pk):
    post = get_object_or_404(Publicacao, pk=pk)
    
    # Criar a visualização da postagem
    Curtida.objects.create(publicacao=post)
    
    # Exibir uma mensagem de sucesso
    messages.success(request, f"🎉 Você curtiu o post {post} com sucesso! 👍")
    
    # Retornar uma resposta simples para não redirecionar a página
    return redirect(reverse_lazy('blog:visualizaPost', kwargs={'pk':pk}))



def comentPost(request, pk):
    post = get_object_or_404(Publicacao, pk=pk)

    if request.method == 'POST':
        form = ComentariosForm(request.POST)

        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            Comentarios.objects.create(publicacao=post, comentario =comentario)
    
            # Exibir uma mensagem de sucesso
            messages.success(request, f"🎉 Você comentou o post {post} com sucesso! 👍")
            
    
            # Retornar uma resposta simples para não redirecionar a página
            return redirect(reverse_lazy('blog:visualizaPost', kwargs={'pk':pk}))
        else:
            messages.error(request, "Ocorreu um erro ao enviar o comentário. Tente novamente")
    else:
        form = ComentariosForm()
    return redirect(reverse_lazy('blog:visualizaPost', kwargs={'pk':pk}))    
