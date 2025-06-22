from django.contrib import admin
from .models import NonConformance, NonConformanceWriteOffItem


# --- Inline para gerenciar os Itens de Baixa dentro da página da Não Conformidade ---
class NonConformanceWriteOffItemInline(admin.TabularInline):
    model = NonConformanceWriteOffItem
    fk_name = 'non_conformance'  # Campo em NonConformanceWriteOffItem que aponta para NonConformance
    extra = 1

    # Adicionamos autocomplete_fields para facilitar a busca por produtos
    autocomplete_fields = ['product_code']

    verbose_name = "Item para Baixa de Estoque"
    verbose_name_plural = "Itens para Baixa de Estoque"


# --- Classe de Administração Principal para a Não Conformidade ---
@admin.register(NonConformance)
class NonConformanceAdmin(admin.ModelAdmin):
    # Configuração da Lista
    list_display = ('description', 'non_conformance_id', 'activity_code', 'company_code')
    list_filter = ('company_code',)
    search_fields = ('description', 'non_conformance_id', 'code')

    # Organização dos Campos no Formulário de Edição
    fieldsets = (
        ('Detalhes da Não Conformidade', {
            'fields': ('description', 'non_conformance_id')
        }),
        ('Vínculos', {
            'fields': ('company_code', 'branch_code', 'activity_code')
        }),
    )

    # Adiciona a seção de Itens de Baixa na página de edição
    inlines = [
        NonConformanceWriteOffItemInline,
    ]


# (Opcional) Registra o modelo de ligação para que tenha sua própria página no admin
@admin.register(NonConformanceWriteOffItem)
class NonConformanceWriteOffItemAdmin(admin.ModelAdmin):
    list_display = ('non_conformance', 'product_code', 'company_code')
    # Facilita a criação/edição ao lidar com listas grandes
    autocomplete_fields = ['non_conformance', 'product_code']
    list_filter = ('company_code', 'branch_code')