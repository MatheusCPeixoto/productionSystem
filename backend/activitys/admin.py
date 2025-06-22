# em activitys/admin.py

from django.contrib import admin
from .models import Activity, ActivitySetup, ActivityEquipment, ActivitySkills

# --- Inlines para os modelos relacionados ---

class ActivitySetupInline(admin.TabularInline):
    model = ActivitySetup
    fk_name = 'activity_code'
    extra = 1
    verbose_name = "Atividade de Setup Requerida"
    verbose_name_plural = "Atividades de Setup Requeridas"
    autocomplete_fields = ['activity_code_setup']

# NOVO: Inline para Equipamentos da Atividade
class ActivityEquipmentInline(admin.TabularInline):
    model = ActivityEquipment
    fk_name = 'activity_code'
    extra = 1
    verbose_name = "Equipamento Requerido"
    verbose_name_plural = "Equipamentos Requeridos"
    # Facilita a seleção de equipamentos se a lista for grande
    autocomplete_fields = ['equipment_code']

# NOVO: Inline para Habilidades da Atividade
class ActivitySkillsInline(admin.TabularInline):
    model = ActivitySkills
    fk_name = 'activity_code'
    extra = 1
    verbose_name = "Habilidade Requerida"
    verbose_name_plural = "Habilidades Requeridas"
    # Facilita a seleção de habilidades
    autocomplete_fields = ['skill_code']


# --- Admin principal para o modelo Activity (ATUALIZADO) ---
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('description', 'activity_id', 'code', 'is_active', 'company_code')
    list_filter = ('is_active', 'company_code')
    search_fields = ('description', 'activity_id', 'code')

    fieldsets = (
        ('Informações Principais', {
            'fields': ('description', 'activity_id', 'is_active')
        }),
        ('Configuração e Vínculos', {
            'fields': ('company_code', 'branch_code', 'setup')
        }),
        ('Instruções de Trabalho (Passos)', {
            'classes': ('collapse',),
            'fields': ('preparation', 'execution', 'verification')
        }),
    )

    # Adicionamos os novos inlines à página de edição da Atividade
    inlines = [
        ActivitySetupInline,
        ActivityEquipmentInline,
        ActivitySkillsInline
    ]

# (Opcional) Registre os modelos de ligação para que tenham sua própria página no admin
# @admin.register(ActivityEquipment)
# class ActivityEquipmentAdmin(admin.ModelAdmin):
#     list_display = ('activity_code', 'equipment_code')
#     autocomplete_fields = ['activity_code', 'equipment_code']
#
# @admin.register(ActivitySkills)
# class ActivitySkillsAdmin(admin.ModelAdmin):
#     list_display = ('activity_code', 'skill_code', 'amount_skills')
#     autocomplete_fields = ['activity_code', 'skill_code']