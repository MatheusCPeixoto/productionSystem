from django.contrib import admin
from .models import (
    OrderActivityProgress,
    ActivityEquipmentLog,
    ActivityWorkforceLog,
    ActivityNonConformanceLog,
    EquipmentStoppageLog,
    WorkforceStoppageLog
)


# --- Inlines para todos os modelos de Log relacionados ao Apontamento ---
# Usamos TabularInline para uma visualização compacta em formato de tabela.

class ActivityWorkforceLogInline(admin.TabularInline):
    model = ActivityWorkforceLog
    fk_name = 'order_activity'
    extra = 0  # Não mostra formulários em branco por padrão
    fields = ('workforce_code', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date')
    autocomplete_fields = ['workforce_code']
    verbose_name_plural = "Logs de Mão de Obra Ativa"


class ActivityEquipmentLogInline(admin.TabularInline):
    model = ActivityEquipmentLog
    fk_name = 'order_activity'
    extra = 0
    fields = ('equipment_code', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date')
    autocomplete_fields = ['equipment_code']
    verbose_name_plural = "Logs de Equipamento Ativo"


class WorkforceStoppageLogInline(admin.TabularInline):
    model = WorkforceStoppageLog
    fk_name = 'order_activity'
    extra = 0
    fields = ('workforce_code', 'stop_reason_code', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date')
    autocomplete_fields = ['workforce_code', 'stop_reason_code']
    verbose_name_plural = "Logs de Parada de Mão de Obra"


class EquipmentStoppageLogInline(admin.TabularInline):
    model = EquipmentStoppageLog
    fk_name = 'order_activity'
    extra = 0
    fields = ('equipment_code', 'stop_reason_code', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date')
    autocomplete_fields = ['equipment_code', 'stop_reason_code']
    verbose_name_plural = "Logs de Parada de Equipamento"


class ActivityNonConformanceLogInline(admin.TabularInline):
    model = ActivityNonConformanceLog
    fk_name = 'order_activity'
    extra = 0
    fields = ('non_conformance', 'quantity')
    autocomplete_fields = ['non_conformance']
    verbose_name_plural = "Logs de Não Conformidade"


# --- Classe de Administração Principal para o Apontamento ---

@admin.register(OrderActivityProgress)
class OrderActivityProgressAdmin(admin.ModelAdmin):
    # Configuração da Lista de Apontamentos
    list_display = ('code', 'order_code', 'activity', 'sequence', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'company_code', 'branch_code', 'activity')
    search_fields = ('code', 'order_code__order_id', 'activity__description')  # Busca em modelos relacionados
    date_hierarchy = 'start_date'
    list_per_page = 20

    # Organização dos Campos no formulário de edição em "Abas"
    fieldsets = (
        ('Informações do Apontamento', {
            'fields': (
                ('order_code', 'activity'),
                ('sequence', 'status'),
                ('start_date', 'end_date'),
                'quantity',
            )
        }),
        ('Vínculos Organizacionais', {
            'classes': ('collapse',),  # Começa recolhido
            'fields': (
                'company_code',
                'branch_code'
            )
        }),
    )

    # Adiciona todas as seções de logs na página de edição
    inlines = [
        ActivityWorkforceLogInline,
        ActivityEquipmentLogInline,
        WorkforceStoppageLogInline,
        EquipmentStoppageLogInline,
        ActivityNonConformanceLogInline,
    ]

    # Torna os campos de data apenas leitura, pois são controlados pelo sistema
    readonly_fields = ('start_date', 'end_date')