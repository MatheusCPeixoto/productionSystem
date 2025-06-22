from django.contrib import admin
from .models import StopReason


@admin.register(StopReason)
class StopReasonAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo StopReason.
    """

    # --- Configuração da Lista de Razões de Parada ---

    # Define as colunas que aparecerão na lista
    list_display = (
        'description',
        'stoppage_id',
        'code',
        'is_active',
        'company_code'
    )

    # Adiciona filtros na barra lateral direita
    list_filter = (
        'is_active',
        'company_code'
    )

    # Habilita a barra de pesquisa no topo da lista.
    # ESSENCIAL para que o autocomplete_fields funcione em outros admins.
    search_fields = (
        'description',
        'stoppage_id',
        'code'
    )

    # --- Organização dos Campos no Formulário de Edição ---
    # Como o modelo é simples, um layout padrão é suficiente,
    # mas podemos usar fieldsets para organizar se desejar.
    fieldsets = (
        (None, {  # 'None' como título remove o cabeçalho da seção
            'fields': (
                'description',
                'stoppage_id',
                'is_active'
            )
        }),
        ('Vínculos Organizacionais', {
            'classes': ('collapse',),  # Seção recolhível
            'fields': (
                'company_code',
                'branch_code'
            )
        }),
    )