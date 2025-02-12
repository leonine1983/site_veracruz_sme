from django.shortcuts import render
from .models import Publicacao

def blog(request):
    context = Publicacao.objects.all()
    return render(request, 'index.html', {'context': context})



