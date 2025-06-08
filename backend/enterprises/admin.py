from django.contrib import admin

from .models import Company, Branch



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'corporate_reason', 'cnpj', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('name',)
    list_per_page = 20
    fieldsets = (
        ('Informações da Empresa', { # Se não usar tradução, pode ser string direta
            'fields': (
                #'code',         # Será somente leitura
                'name',
                'corporate_reason',
                'cnpj',
                'ie',
                'is_active'
            )
        }),
        ('Endereço', {
            'fields': (
                'street',
                'street_number',
                'neighborhood',
                'city',
                'uf',
                'zip_code',
                'country'
            )
        }),
        ('Contato e Mídia', {
            'fields': (
                'phone',
                'fax',
                'logo',
                'key'
            )
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'cnpj', 'corporate_reason', 'is_main')
    search_fields = ('corporate_reason',)
    list_filter = ('is_main',)
    ordering = ('corporate_reason',)
    list_per_page = 20
    fieldsets = (
        ('Identificação da Filial', {
            'fields': (
                'company_code',  # Exibe o nome da empresa associada
                #'code',  # Será somente leitura
                'fantasy_name',
                'corporate_reason',
                'cnpj',
                'ie',
                'im',
                'is_main',
                'branch_activity',
                'code_main_activity',
                'description_main_activity',
                'federal_activity_code',
                'suframa',
                'path_logo'
            )
        }),
        ('Endereço', {
            'fields': (
                'zip_code',
                'street',
                'street_number',
                'complement',
                'neighborhood',
                'municipality_code', # Se for usar, descomente e adicione aqui
                'uf',
                'country',
                'mailbox'
            )
        }),
        ('Contato', {
            'fields': (
                'phone',
                'fax',
                'email',
                'contact'
            )
        }),
        ('Dados Fiscais (Documentos Eletrônicos)', {
            'fields': (
                'tax_regime',
                'type_certificate',
                'nfe_certificate',
                'nfe_danfe',
                'nfe_xml_authorized',
                'default_nfe_directory',
                'technical_manager_nfe',
                'nfce_danfce',
                'nfce_csc',
                'nfce_id_token',
                'activation_code_sat',
                'signature_sat',
                'issuer_type_mdfe',
                'series_code_mdfe',
                'mdfe_rntrc',
                'mdfe_damdfe',
                'nfse_login',
                'nfse_password',
                'nfse_cpf_user'
            )
        }),
        ('Configurações SPED', {
            'fields': (
                'sped_ind_perfil',
                'sped_ind_ativ',
                'sped_pc_ind_nat_pj',
                'sped_pc_cod_inc_trib',
                'sped_pc_cod_tipo_cont',
                'sped_pc_ind_apro_cred',
                'sped_pc_ind_reg_cum'
            )
        }),
        ('Alíquotas, Regimes e Cadastros Auxiliares', {
            'fields': (
                'is_rural_producer',
                'simple_credit_aliquot',
                'aliquot_iss',
                'is_end_consumer_interstate_icms',
                'uses_cest',
                'regional_council_number',
                'regional_council_date'
            )
        }),
        ('Informações do Contabilista', {
            'fields': (
                'accountant_name',
                'accountant_cpf',
                'accountant_crc',
                'accountant_cnpj',
                'accountant_zip_code',
                'accountant_street',
                'accountant_street_number',
                'accountant_complement',
                'accountant_neighborhood',
                'accountant_phone',
                'accountant_fax',
                'accountant_email',
                'accountant_code_municipality', # Se for usar, descomente
            )
        }),
        ('Integrações e API', {
            'fields': (
                'status_api_payments',
                'code_account_api_payments',
                'token_api_payments',
                'send_proof_pay_email_api',
                'cnpj_payer_api_payment',
                'id_api_connection_integration_nfe',
                'user_api_blumetalk',
                'password_api_blumetalk',
                'integration_bases_wmw'
            )
        }),
        ('Configurações Financeiras e Contratuais', {
            'fields': (
                'cf_despesasfv',
                'cf_custofv',
                'ie_auxiliary',
                'cf_other_expenses',
                'code_bill_account',
                'contract_holder',
                'cnpj_contract',
                'cpf_contract'
            )
        }),
        ('Parâmetros de Utilização (Flags)', {
            'fields': (
                'uses_certificate',
                'uses_calculus_inside',
                'use_report_filter',
                'use_cfs_grid_product',
                'uses_aliquot_by_region',
                'qrcode_side',
                'uses_date_filter_finan',
                'uses_larger_obs_danfe',
                'uses_partial_credit_card',
                'use_low_block_finan',
                'uses_annual_data_movements',
                'uses_history_product_search',
                'use_confirmation_general_search',
                'uses_cliforn_global_standard',
                'uses_global_default_product'
            )
        })
    )
