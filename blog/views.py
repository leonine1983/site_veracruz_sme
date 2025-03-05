from django.shortcuts import render
from .models import Publicacao, PastaAdministrativa, Secretario
from dashboard.models import Link

def blog(request):
    secretario = Secretario.objects.all()

    if 'secretario' in request.GET:
        request.session.flush()
        id = request.GET['secretario']
        secretario = Secretario.objects.filter(id=id)
        request.session['secretario'] = secretario
        publica = Publicacao.objects.filter(secretario__id = id)
    else:        
        request.session['secretario'] = secretario
        publica = Publicacao.objects.filter(secretario__ativo = True)




   

    



    context = publica
    links = Link.objects.all()    
    footer = PastaAdministrativa.objects.get(nome_filter = "educação")    
    request.session['links'] = links
    request.session['publica'] = context
    request.session['footer'] = footer
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
        'context': context,
        'links': links,
        "colors": colors})



