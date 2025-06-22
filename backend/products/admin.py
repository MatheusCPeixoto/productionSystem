from django.contrib import admin

from .models import Product, ProductFile, ProductCode, ProductBranch


class ProductFileInline(admin.TabularInline): # Ou admin.StackedInline para um layout diferente
    model = ProductFile
    extra = 1  # Quantos formulários de upload em branco aparecerão por padrão
    fields = ('name', 'file_type', 'activity', 'file') # Campos a serem exibidos


class ProductCodeInline(admin.TabularInline):
    model = ProductCode
    # Campos que aparecerão para cada código similar
    fields = ('similar_code', 'sale_price')
    extra = 1  # Quantos formulários em branco para adicionar novos códigos
    verbose_name = "Código Similar"
    verbose_name_plural = "Códigos Similares"


class ProductBranchInline(admin.TabularInline):
    model = ProductBranch
    fields = ('branch_code', 'balance', 'minimum_stock', 'maximum_stock')
    extra = 1
    verbose_name = "Estoque por Filial"
    verbose_name_plural = "Estoques por Filial"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # --- Configuração da Lista de Produtos ---
    list_display = ('name', 'product_identifier', 'code', 'is_inactive')
    list_filter = ('is_inactive', 'group_code')
    search_fields = ('name', 'product_identifier', 'code', 'technical_description')

    # --- Organização dos Campos em "Abas" (Fieldsets) ---
    # Cada tupla é um fieldset. O primeiro item é o título da "aba".
    # {'classes': ('collapse',)} faz a seção ser recolhível, criando o efeito de aba.
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                'name',
                'product_identifier',
                'technical_description',
                'is_inactive',
                'type',
                'brand',
                'size',
                'image_path'
            )
        }),
        ('Classificação e Hierarquia', {
            'classes': ('collapse',),  # Começa recolhido
            'fields': (
                'group_code',
                'subgroup_code',
                'family_code1',
                'family_code2',
                'family_code3',
                'family_code4',
                'family_code5',
                'parent_product_code',
            )
        }),
        ('Unidades e Medidas', {
            'classes': ('collapse',),
            'fields': (
                ('control_unit_code', 'control_unit_symbol'),
                ('purchase_unit_code', 'purchase_unit_symbol'),
                ('sale_unit_code', 'sale_unit_symbol'),
                ('net_weight', 'gross_weight'),
                ('length', 'width', 'height', 'thickness'),
                'diameter',
            )
        }),
        ('Controle de Estoque', {
            'classes': ('collapse',),
            'fields': (
                'minimum_stock',
                'maximum_stock',
                'reorder_point',
                'lead_time',
                'validity_days',
                'uses_batch',
                'uses_nfe_batch',
                'no_stock_control',
                'ignore_inventory',
            )
        }),
        ('Preços e Custos', {
            'classes': ('collapse',),
            'fields': (
                'average_cost',
                'sale_price',
                'minimum_selling_price',
                'price1',
                'price2',
                'price3',
            )
        }),
        ('Informações Fiscais e Tributárias', {
            'classes': ('collapse',),
            'fields': (
                'ncm_code',
                'tax_classification',
                'origin',
                'ipi_tax_situation',
                'ipi_entry_tax_situation',
                'tax_benefit_code',
                'sped_item_type_id',
            )
        }),
        ('Campos Livres (Customizados)', {
            'classes': ('collapse',),
            'fields': (
                ('free_field1', 'free_field2', 'free_field3'),
                ('free_field4', 'free_field5'),
                ('free_date1', 'free_date2', 'free_date3'),
                ('free_date4', 'free_date5'),
                ('free_value1', 'free_value2', 'free_value3'),
                ('free_value4', 'free_value5'),
            )
        }),
    )

    # --- Seções para os modelos relacionados ---
    inlines = [
        ProductCodeInline,
        ProductBranchInline,
    ]

# Você também pode registrar o ProductFile separadamente se quiser uma página só para ele
@admin.register(ProductFile)
class ProductFileAdmin(admin.ModelAdmin):
    # --- OTIMIZAÇÕES DE PERFORMANCE PARA A LISTA ---

    # 1. Paginação: Esta é a mudança mais importante.
    # Em vez de carregar TODOS os arquivos de uma vez, o admin vai carregar
    # apenas 25 por página. Isso reduz drasticamente a carga inicial.
    list_per_page = 25

    # 2. Otimização de Filtro (ForeignKey):
    # O filtro por 'product' pode ser lento se houver muitos produtos.
    # Usar 'raw_id_fields' transforma o dropdown de filtro em um campo de ID,
    # que é muito mais rápido. O usuário digita o ID do produto para filtrar.
    # Se você não usa muito esse filtro, pode até removê-lo de 'list_filter'.
    raw_id_fields = ('product',)

    # ---------------------------------------------------

    # Configurações que já tínhamos:
    list_display = ('name', 'product', 'file_type', 'display_activities')
    list_filter = ('file_type', 'product')  # O filtro 'product' agora será mais rápido
    autocomplete_fields = ['product', 'activities']
    search_fields = ('name', 'product__name', 'activities__description')
    list_select_related = ['product']
    prefetch_related = ['activities']

    def display_activities(self, obj):
        # ... (seu método display_activities como antes) ...
        activities = obj.activities.all()[:3]
        if not activities:
            return "Todas as Atividades"

        activity_names = ", ".join([a.description for a in activities])

        if obj.activities.count() > 3:
            return f"{activity_names}..."
        return activity_names

    display_activities.short_description = 'Atividades Específicas'
