from django.contrib import admin
from django.db import models
from .models import ProductionCalendar, ShiftNonWorkingDay


# --- Inline para gerenciar os Dias Não Úteis dentro da página do Calendário ---
# Usamos TabularInline para uma visualização compacta em formato de tabela.
class ShiftNonWorkingDayInline(admin.TabularInline):
    model = ShiftNonWorkingDay
    fields = ('non_working_day', 'start_time', 'end_time', 'description')
    extra = 1
    verbose_name = "Dia/Turno Não Útil"
    verbose_name_plural = "Dias e Turnos Não Úteis"

    # --- CORREÇÃO APLICADA AQUI ---
    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'size': '20'})},
        models.DateTimeField: {'widget': admin.widgets.AdminDateWidget(attrs={'size': '10'})},
    }


# --- Classe de Administração Principal para o Calendário de Produção ---
@admin.register(ProductionCalendar)
class ProductionCalendarAdmin(admin.ModelAdmin):
    # Configuração da Lista de Calendários
    list_display = ('description', 'year', 'company_code', 'branch_code')
    list_filter = ('year', 'company_code')
    search_fields = ('description', 'year')

    # Organização dos Campos em "Abas" (Fieldsets)
    fieldsets = (
        (None, {  # Uma seção principal sem título
            'fields': (
                'description',
                'year',
                'start_date'
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

    # Adiciona a seção de Dias Não Úteis à página de edição do Calendário
    inlines = [
        ShiftNonWorkingDayInline,
    ]


# (Opcional) Registra o modelo de ligação para que tenha sua própria página no admin
@admin.register(ShiftNonWorkingDay)
class ShiftNonWorkingDayAdmin(admin.ModelAdmin):
    list_display = ('non_working_day', 'description', 'production_calendar')
    list_filter = ('production_calendar',)
    search_fields = ('description',)