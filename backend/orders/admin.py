from django.contrib import admin
from .models import Order, OrderItem, OrderPlannedMaterial


# --- Inlines para os modelos relacionados à Ordem ---

class OrderItemInline(admin.TabularInline):
    """
    Permite visualizar e editar os Itens da Ordem diretamente na página da Ordem.
    """
    model = OrderItem
    fk_name = 'order_code'  # Campo em OrderItem que aponta para Order

    # Campos exibidos no inline
    fields = ('structure_code', 'planned_quantity', 'completed_quantity', 'necessity_date')

    # Facilita a seleção da estrutura, caso a lista seja grande
    autocomplete_fields = ['structure_code']

    extra = 1  # Mostra um formulário em branco para adicionar um novo item
    verbose_name = "Item da Ordem"
    verbose_name_plural = "Itens da Ordem"


class OrderPlannedMaterialInline(admin.TabularInline):
    """
    Permite visualizar e editar os Materiais Previstos diretamente na página da Ordem.
    """
    model = OrderPlannedMaterial
    fk_name = 'order_code'  # Campo em OrderPlannedMaterial que aponta para Order

    fields = ('raw_material', 'quantity', 'workstation_code', 'necessity_start_date')

    # Facilita a seleção de matéria-prima e posto de trabalho
    autocomplete_fields = ['raw_material', 'workstation_code']

    extra = 1
    verbose_name = "Material Previsto"
    verbose_name_plural = "Materiais Previstos para a Ordem"


# --- Classe de Administração Principal para a Ordem ---

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Configuração da Lista de Ordens
    list_display = ('order_id', 'order_description', 'status', 'opening_date', 'closing_date')
    list_filter = ('status', 'company_code', 'branch_code')
    search_fields = ('order_id', 'code', 'order_description')
    date_hierarchy = 'opening_date'  # Adiciona uma navegação por datas

    # Organização dos Campos do formulário em "Abas" (Fieldsets)
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                ('order_id', 'status'),
                'order_description',
                'responsible',
            )
        }),
        ('Datas e Prazos', {
            'fields': (
                ('opening_date', 'closing_date'),
                'last_recalculation_date',
            )
        }),
        ('Configuração e Tipos', {
            'classes': ('collapse',),  # Seção recolhível
            'fields': (
                'company_code',
                'branch_code',
                'order_type',
                'programming_type',
                'necessity_origin',
            )
        }),
        ('Quantidades e Custos', {
            'classes': ('collapse',),
            'fields': (
                'planned_quantity',
                'posted_quantity',
                'order_cost',
                'proportionality',
            )
        }),
        ('Observações', {
            'classes': ('collapse',),
            'fields': (
                'order_observation',
            )
        }),
    )

    # Adiciona as seções de Itens e Materiais na página de edição da Ordem
    inlines = [
        OrderItemInline,
        OrderPlannedMaterialInline,
    ]


# (Opcional) Registre os outros modelos para terem suas próprias páginas no admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'order_code', 'structure_code', 'planned_quantity')
    autocomplete_fields = ['order_code', 'structure_code']


@admin.register(OrderPlannedMaterial)
class OrderPlannedMaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'order_code', 'raw_material', 'quantity')
    autocomplete_fields = ['order_code', 'raw_material']