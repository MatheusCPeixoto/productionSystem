from django.contrib import admin
from .models import Structure, StructureActivity


# --- Inline para gerenciar as Atividades da Estrutura ---
class StructureActivityInline(admin.TabularInline):
    """
    Permite adicionar/editar as atividades diretamente na página da Estrutura.
    """
    model = StructureActivity
    fk_name = 'structure_code'  # Campo em StructureActivity que aponta para Structure

    # Campos a serem exibidos no formulário inline
    fields = ('sequence', 'activity_code', 'workstation_code', 'process_time', 'cycle_time')

    # Facilita a seleção de atividades e postos de trabalho
    autocomplete_fields = ['activity_code', 'workstation_code']

    extra = 1  # Mostra um formulário em branco para adicionar uma nova atividade
    verbose_name = "Atividade da Estrutura"
    verbose_name_plural = "Atividades da Estrutura"
    # Ordena as atividades pela sequência dentro do admin
    ordering = ('sequence',)


# --- Classe de Administração Principal para a Estrutura ---
@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    # Configuração da Lista de Estruturas
    list_display = ('description', 'structure_id', 'product_code', 'is_active_flag1')
    list_filter = ('is_active_flag1', 'company_code')
    search_fields = ('description', 'structure_id', 'code', 'product_code__name')  # Permite buscar pelo nome do produto

    # Organização dos Campos do formulário em "Abas" (Fieldsets)
    fieldsets = (
        ('Identificação Principal', {
            'fields': (
                'description',
                'structure_id',
                'product_code',
                ('is_active_flag1', 'is_active_flag2', 'is_main'),
            )
        }),
        ('Hierarquia e Vínculos', {
            'classes': ('collapse',),
            'fields': (
                'parent_structure',
                'company_code',
                'branch_code',
                'user_code',
                'revision_number',
            )
        }),
        ('Custos e Quantidades', {
            'classes': ('collapse',),
            'fields': (
                'indirect_cost',
                'planned_structure_cost',
                'loss_percentage',
                'mrp_orders_balance',
            )
        }),
        ('Dados Técnicos', {
            'classes': ('collapse',),
            'fields': (
                'tech_data_multiple_quantity',
                'tech_data_multiple_standard_width',
                'tech_data_multiple_standard_length',
                'gear_validation',
                'wing_or_handle',
                'z_factor'
            )
        }),
        ('Observações', {
            'classes': ('collapse',),
            'fields': (
                'observation',
                'image_address',
            )
        }),
    )

    # Adiciona a seção de Atividades da Estrutura na página de edição
    inlines = [
        StructureActivityInline,
    ]


# (Opcional) Registra o modelo StructureActivity para ter sua própria página no admin
@admin.register(StructureActivity)
class StructureActivityAdmin(admin.ModelAdmin):
    list_display = ('structure_code', 'sequence', 'activity_code', 'workstation_code')
    list_filter = ('structure_code__product_code',)  # Filtra por produto da estrutura
    search_fields = ('structure_code__description', 'activity_code__description')
    autocomplete_fields = ['structure_code', 'activity_code', 'workstation_code']