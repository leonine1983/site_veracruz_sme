from django.contrib import admin
from .models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('nome', 'url', 'descricao')
    search_fields = ('nome',)
    list_filter = ('nome',)

admin.site.register(Link, LinkAdmin)





