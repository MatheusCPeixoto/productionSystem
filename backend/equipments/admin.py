from django.contrib import admin
from .models import Equipment, CompositeEquipment, EquipmentSkill, EquipmentCostHistory


# --- Inlines para os modelos relacionados ---
# Usamos inlines para editar modelos relacionados diretamente na página do modelo principal (Equipment).

class ChildEquipmentInline(admin.TabularInline):
    """ Inline para mostrar/adicionar os 'filhos' de um equipamento pai. """
    model = CompositeEquipment
    fk_name = 'parent_equipment_code'  # Liga ao equipamento que estamos editando como 'pai'
    verbose_name = "Componente Filho"
    verbose_name_plural = "Componentes (Filhos)"
    extra = 1
    # Facilita a busca pelo equipamento filho a ser adicionado
    autocomplete_fields = ['child_equipment_code']


class ParentEquipmentInline(admin.TabularInline):
    """ Inline para mostrar de qual equipamento 'pai' este equipamento faz parte. """
    model = CompositeEquipment
    fk_name = 'child_equipment_code'  # Liga ao equipamento que estamos editando como 'filho'
    verbose_name = "Parte do Equipamento Pai"
    verbose_name_plural = "Parte dos Equipamentos (Pais)"
    extra = 1
    autocomplete_fields = ['parent_equipment_code']


class EquipmentSkillInline(admin.TabularInline):
    """ Inline para gerenciar as habilidades necessárias para o equipamento. """
    model = EquipmentSkill
    fk_name = 'equipment_code'
    extra = 1
    verbose_name = "Habilidade Requerida"
    verbose_name_plural = "Habilidades Requeridas"
    autocomplete_fields = ['skill_code']


class EquipmentCostHistoryInline(admin.TabularInline):
    """ Inline para visualizar o histórico de custos do equipamento. """
    model = EquipmentCostHistory
    fk_name = 'equipment_code'
    extra = 1
    fields = ('month', 'year', 'hourly_cost', 'monthly_cost', 'is_current')
    verbose_name = "Histórico de Custo"
    verbose_name_plural = "Históricos de Custo"


# --- Classe de Administração Principal para o Modelo Equipment ---
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    # Configuração da Lista de Equipamentos
    list_display = ('description', 'equipment_id', 'workstation_code', 'code')
    list_filter = ('workstation_code', 'company_code')
    search_fields = ('description', 'equipment_id', 'code', 'address')

    # Organização dos Campos em "Abas" (Fieldsets)
    fieldsets = (
        ('Identificação Principal', {
            'fields': (
                'description',
                'equipment_id',
                ('company_code', 'branch_code'),
                'workstation_code',
            )
        }),
        ('Detalhes e Especificações', {
            'classes': ('collapse',),  # Começa recolhido
            'fields': (
                'type',
                'address',
                'equipment_observation',
                'utility_notes',
                'usage_notes'
            )
        }),
        ('Custos e Performance', {
            'classes': ('collapse',),
            'fields': (
                'hourly_cost',
                'monthly_cost',
                'effectiveness',
                'hourly_production',
                'daily_efficiency',
                'monthly_efficiency',
            )
        }),
    )

    # Seções para os modelos relacionados que aparecerão na página de edição
    inlines = [
        ChildEquipmentInline,
        ParentEquipmentInline,
        EquipmentSkillInline,
        EquipmentCostHistoryInline,
    ]