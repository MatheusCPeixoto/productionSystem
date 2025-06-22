from django.contrib import admin
from .models import Workstation

@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo Workstation.
    """

    # --- Configuração da Lista de Postos de Trabalho ---
    list_display = (
        'description',
        'code',
        'is_active',
        'cost_center_code',
        'company_code'
    )
    list_filter = (
        'is_active',
        'is_external',
        'company_code',
        'branch_code'
    )
    search_fields = (
        'description',
        'code',
        'cost_center_code'
    )

    # --- Organização dos Campos no Formulário de Edição em "Abas" (Fieldsets) ---
    fieldsets = (
        ('Identificação Principal', {
            'fields': (
                'description',
                ('is_active', 'is_external'),
                'cost_center_code',
            )
        }),
        ('Configuração de Calendários', {
            'description': "Associe os calendários a este posto de trabalho. O autocomplete ajuda a pesquisar.",
            'fields': (
                'production_calendar',
                'calendar1',
                'calendar2',
            )
        }),
        ('Custos e Performance', {
            'classes': ('collapse',),  # Seção recolhível
            'fields': (
                'hourly_cost',
                'monthly_cost',
                'effectiveness',
            )
        }),
        ('Vínculos Organizacionais e Outros', {
            'classes': ('collapse',),
            'fields': (
                'company_code',
                'branch_code',
                'stock_location_code',
                'cost_sql',
            )
        }),
    )

    # Transforma os campos de seleção de Calendário em campos de busca
    autocomplete_fields = [
        'production_calendar',
        'calendar1',
        'calendar2',
        'company_code', # Adicionado para consistência
        'branch_code'   # Adicionado para consistência
    ]