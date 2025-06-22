from django.contrib import admin
from .models import Workforce, WorkforceCostHistory, Skill, WorkforceSkill


# --- Inlines para os modelos relacionados à Mão de Obra (Workforce) ---

class WorkforceSkillInline(admin.TabularInline):
    """ Permite associar habilidades diretamente na página do funcionário. """
    model = WorkforceSkill
    fk_name = 'workforce_code'
    extra = 1
    autocomplete_fields = ['skill']  # Facilita a busca por habilidades
    verbose_name = "Habilidade Associada"
    verbose_name_plural = "Habilidades Associadas"


class WorkforceCostHistoryInline(admin.TabularInline):
    """ Mostra o histórico de custos diretamente na página do funcionário. """
    model = WorkforceCostHistory
    fk_name = 'workforce_code'
    extra = 0  # Histórico geralmente não é adicionado manualmente aqui
    fields = ('month', 'year', 'hourly_cost', 'monthly_cost', 'is_current')
    readonly_fields = ('month', 'year', 'hourly_cost', 'monthly_cost', 'is_current')
    verbose_name = "Histórico de Custo"
    verbose_name_plural = "Históricos de Custo"

    # Impede que novos históricos sejam adicionados por aqui
    def has_add_permission(self, request, obj=None):
        return False


# --- Classe de Administração Principal para Mão de Obra (Workforce) ---

@admin.register(Workforce)
class WorkforceAdmin(admin.ModelAdmin):
    # Configuração da Lista
    list_display = ('name', 'workforce_id_text', 'badge_number', 'is_active', 'company_code')
    list_filter = ('is_active', 'company_code', 'branch_code')
    search_fields = ('name', 'workforce_id_text', 'badge_number', 'cpf')

    # Organização do Formulário em "Abas" (Fieldsets)
    fieldsets = (
        ('Identificação Principal', {
            'fields': (
                'name',
                ('workforce_id_text', 'badge_number', 'employee_id_plate'),
                'is_active'
            )
        }),
        ('Informações Pessoais', {
            'classes': ('collapse',),
            'fields': (
                ('cpf', 'rg'),
                'birth_date',
                'father_name',
                'mother_name'
            )
        }),
        ('Contato e Endereço', {
            'classes': ('collapse',),
            'fields': (
                'street',
                'street_number',
                'neighborhood',
                'city_code',
                'state_uf',
                'zip_code',
                ('phone1', 'phone2')
            )
        }),
        ('Dados de Custo e Performance', {
            'classes': ('collapse',),
            'fields': (
                'hourly_cost',
                'monthly_cost',
                'effectiveness',
                'daily_efficiency',
                'monthly_efficiency'
            )
        }),
        ('Vínculos e Configurações', {
            'classes': ('collapse',),
            'fields': (
                'company_code',
                'branch_code',
                'cf_sector',
                'cf_situation'
            )
        }),
    )

    # Seções de modelos relacionados
    inlines = [
        WorkforceSkillInline,
        WorkforceCostHistoryInline,
    ]


# --- Admin para o modelo de Habilidades (Skill) ---
# Essencial para que o autocomplete_fields funcione no WorkforceAdmin

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ('description', 'code')
    list_display = ('description', 'code', 'is_active')
    list_filter = ('is_active', 'company_code')