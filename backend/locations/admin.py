from django.contrib import admin
from .models import Country, State, Municipality

# --- Inline para gerenciar os Municípios dentro da página do Estado ---
class MunicipalityInline(admin.TabularInline):
    model = Municipality
    fk_name = 'code_state' # O campo em Municipality que aponta para State
    fields = ('name', 'identifier')
    extra = 1
    verbose_name = "Município"
    verbose_name_plural = "Municípios do Estado"


# --- Admin para o modelo Country (País) ---
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # Habilita a pesquisa por nome e identificador
    search_fields = ('name', 'identifier')
    list_display = ('name', 'identifier', 'code')


# --- Admin para o modelo State (Estado/UF) ---
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    # Habilita a pesquisa, crucial para o autocomplete no MunicipalityAdmin
    search_fields = ('name', 'identifier')
    list_display = ('name', 'identifier', 'code_country')
    list_filter = ('code_country',) # Permite filtrar estados por país

    # Adiciona a lista de municípios na página de edição do estado
    inlines = [
        MunicipalityInline,
    ]


# --- Admin para o modelo Municipality (Município) ---
@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_state')
    search_fields = ('name', 'identifier')
    list_filter = ('code_state__code_country', 'code_state') # Permite filtrar por país e depois por estado

    # Transforma o campo de seleção de Estado em um campo de busca,
    # muito melhor que um dropdown gigante.
    autocomplete_fields = ['code_state']