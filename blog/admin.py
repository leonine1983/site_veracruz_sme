from django.contrib import admin
from .models import Ano, Prefeitura, Secretario, TipoPublicacao, Publicacao, PastaAdministrativa, ViewsPost, Comentarios

# Registro dos modelos
class PrefeituraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prefeito', 'ano')
    search_fields = ('nome', 'prefeito')
    list_filter = ('ano',)

class SecretarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pasta', 'prefeitura', 'data_inicio', 'data_fim')
    search_fields = ('nome', 'pasta')
    list_filter = ('prefeitura',)

class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'tipo_publicacao', 'secretario')
    search_fields = ('titulo', 'descricao')
    list_filter = ('tipo_publicacao', 'secretario', 'data_publicacao')
    readonly_fields = ('descricao',)  # Para impedir edição direta no campo de descrição

class ViewsPostAdmin(admin.ModelAdmin):
    list_display = ('publicacao', 'data_view')
    search_fields = ('publicacao', 'data_view')
    list_filter = ('publicacao', 'data_view')
    readonly_fields = ('publicacao',)  # Para impedir edição direta no campo de descrição
    

class TipoPublicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class PastaAdministrativa_Admin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class AnoAdmin(admin.ModelAdmin):
    list_display = ('ano',)
    search_fields = ('ano',)



# Registrando os modelos no admin
admin.site.register(Ano, AnoAdmin)
admin.site.register(Prefeitura, PrefeituraAdmin)
admin.site.register(PastaAdministrativa, PastaAdministrativa_Admin)
admin.site.register(Secretario, SecretarioAdmin)
admin.site.register(TipoPublicacao, TipoPublicacaoAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
admin.site.register(ViewsPost, ViewsPostAdmin)
admin.site.register(Comentarios)

