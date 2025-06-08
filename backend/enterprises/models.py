from django.db import models


class Company(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    name = models.CharField(
        db_column='NOME',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Nome'
    )  # Field name made lowercase.
    is_active = models.IntegerField(
        db_column='ATIVA',
        blank=True,
        null=True,
        verbose_name='Ativa'
    )  # Field name made lowercase.
    cnpj = models.CharField(
        db_column='CNPJ',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ'
    )  # Field name made lowercase.
    ie = models.CharField(
        db_column='IE',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Inscrição Estadual'
    )  # Field name made lowercase.
    street = models.CharField(
        db_column='RUA',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Rua'
    )  # Field name made lowercase.
    street_number = models.CharField(
        db_column='NUMERO',
        max_length=6,
        blank=True,
        null=True,
        verbose_name='Número'
    )  # Field name made lowercase.
    neighborhood = models.CharField(
        db_column='BAIRRO',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Bairro'
    )  # Field name made lowercase.
    city = models.CharField(
        db_column='CIDADE',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Cidade'
    )  # Field name made lowercase.
    uf = models.CharField(
        db_column='UF',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='UF'
    )  # Field name made lowercase.
    zip_code = models.CharField(
        db_column='CEP',
        max_length=9,
        blank=True,
        null=True,
        verbose_name='CEP'
    )  # Field name made lowercase.
    country = models.CharField(
        db_column='PAIS',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='País'
    )  # Field name made lowercase.
    phone = models.CharField(
        db_column='TELEFONE',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )  # Field name made lowercase.
    fax = models.CharField(
        db_column='FAX',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Fax'
    )  # Field name made lowercase.
    logo = models.CharField(
        db_column='LOGOMARCA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Logomarca'
    )  # Field name made lowercase.
    image = models.BinaryField(
        db_column='IMAGEM',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )  # Field name made lowercase.
    key = models.TextField(
        db_column='CHAVE',
        blank=True,
        null=True,
        verbose_name='Chave'
    )  # Field name made lowercase. This field type is a guess.
    corporate_reason = models.CharField(
        db_column='RAZAOSOCIAL',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Razão Social'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COLIGADA'
        verbose_name = 'Coligada'
        verbose_name_plural = 'Coligadas'

    def __str__(self):
        return self.name if self.name else f"Coligada {self.code}"


class Branch(models.Model):
    company_code = models.ForeignKey(
        'Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Código Coligada'
    )
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )
    cnpj = models.CharField(
        db_column='CNPJ',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ'
    )
    corporate_reason = models.CharField(
        db_column='RAZAOSOCIAL',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Razão Social'
    )
    ie = models.CharField(
        db_column='INSCRICAOESTADUAL',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Inscrição Estadual'
    )
    phone = models.CharField(
        db_column='TELEFONE',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )
    fax = models.CharField(
        db_column='FAX',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Fax'
    )
    email = models.CharField(
        db_column='EMAIL',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='E-mail'
    )
    street = models.CharField(
        db_column='RUA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Rua'
    )
    street_number = models.CharField(
        db_column='NUMERO',
        max_length=8,
        blank=True,
        null=True,
        verbose_name='Número'
    )
    complement = models.CharField(
        db_column='COMPLEMENTO',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Complemento'
    )
    neighborhood = models.CharField(
        db_column='BAIRRO',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Bairro'
    )
    municipality_code = models.ForeignKey(
        'locations.Municipality',
        models.DO_NOTHING,
        db_column='CODCIDADE',
        blank=True,
        null=True,
        verbose_name='Código Cidade',
        related_name='filial_municipio_codigo_one_set'
    )
    uf = models.CharField(
        db_column='UF',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='UF'
    )
    country = models.CharField(
        db_column='PAIS',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='País'
    )
    zip_code = models.CharField(
        db_column='CEP',
        max_length=9,
        blank=True,
        null=True,
        verbose_name='CEP'
    )
    contact = models.CharField(
        db_column='CONTATO',
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Contato'
    )
    is_rural_producer = models.SmallIntegerField(
        db_column='PRODUTORRURAL',
        blank=True,
        null=True,
        verbose_name='É Produtor Rural'
    )
    branch_activity = models.CharField(
        db_column='RAMOATIVIDADE',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Atividade da Filial'
    )
    im = models.CharField(
        db_column='INSCMUN',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Inscrição Municipal'
    )
    federal_activity_code = models.CharField(
        db_column='CODATIVFED',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Atividade Federal'
    )
    code_main_activity = models.CharField(
        db_column='CODATIVIDPRINC',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Código Atividade Principal'
    )
    description_main_activity = models.CharField(
        db_column='DESCATIVIDPRINC',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição Atividade Principal'
    )
    regional_council_number = models.CharField(
        db_column='NUMREGJUNTA',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Número Junta Regional'
    )
    mailbox = models.CharField(
        db_column='CAIXAPOSTAL',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Caixa Postal'
    )
    regional_council_date = models.DateTimeField(
        db_column='DATAREGJUNTA',
        blank=True,
        null=True,
        verbose_name='Data Junta Regional'
    )  # Field name made lowercase.
    suframa = models.CharField(
        db_column='SUFRAMA',
        max_length=14,
        blank=True,
        null=True,
        verbose_name='SUFRAMA'
    )
    fantasy_name = models.CharField(
        db_column='NOMEFANTASIA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome Fantasia'
    )
    is_main = models.IntegerField(
        db_column='PRINCIPAL',
        blank=True,
        null=True,
        verbose_name='É Principal'
    )
    code_municipality = models.ForeignKey(
        'locations.Municipality',
        models.DO_NOTHING,
        db_column='CODIGO_MUNICIPIOS',
        blank=True,
        null=True,
        verbose_name='Código Município',
        related_name='filial_codigo_municipios_two_set'
    )
    cf_despesasfv = models.CharField(
        db_column='CF_DESPESASFV',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Despesas FV'
    )
    cf_custofv = models.CharField(
        db_column='CF_CUSTOFV',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Custo FV'
    )
    ie_auxiliary = models.CharField(
        db_column='INSCRICAOESTADUAL_AUXILIAR',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Inscrição Estadual Auxiliar'
    )
    cf_other_expenses = models.CharField(
        db_column='CF_OUTRAS_DESPEAS',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Outras Despesas'
    )
    tax_regime = models.IntegerField(
        db_column='REGIME_TRIBUTARIO',
        blank=True,
        null=True,
        verbose_name='Regime Tributário'
    )
    nfe_certificate = models.CharField(
        db_column='NFE_CERTIFICADO',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='NFE Certificado'
    )
    nfe_danfe = models.CharField(
        db_column='NFE_DANFE',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='NFE DANFE'
    )
    type_certificate = models.IntegerField(
        db_column='TIPO_CERTIFICADO',
        blank=True,
        null=True,
        verbose_name='Tipo de Certificado'
    )
    simple_credit_aliquot = models.DecimalField(
        db_column='ALIQUOTA_CREDITO_SIMPLES',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Alíquota Crédito Simples'
    )
    accountant_name = models.CharField(
        db_column='CONTABILISTA_NOME',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome do Contabilista'
    )
    accountant_cpf = models.CharField(
        db_column='CONTABILISTA_CPF',
        max_length=14,
        blank=True,
        null=True,
        verbose_name='CPF do Contabilista'
    )
    accountant_crc = models.CharField(
        db_column='CONTABILISTA_CRC',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='CRC do Contabilista'
    )
    accountant_cnpj = models.CharField(
        db_column='CONTABILISTA_CNPJ',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ do Contabilista'
    )
    accountant_zip_code = models.CharField(
        db_column='CONTABILISTA_CEP',
        max_length=9,
        blank=True,
        null=True,
        verbose_name='CEP do Contabilista'
    )
    accountant_street = models.CharField(
        db_column='CONTABILISTA_RUA',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Rua do Contabilista'
    )
    accountant_street_number = models.CharField(
        db_column='CONTABILISTA_NUMERO',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Número da casa do Contabilista'
    )
    accountant_complement = models.CharField(
        db_column='CONTABILISTA_COMPLEMENTO',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Complemento do Contabilista'
    )
    accountant_neighborhood = models.CharField(
        db_column='CONTABILISTA_BAIRRO',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Bairro do Contabilista'
    )
    accountant_phone = models.CharField(
        db_column='CONTABILISTA_TELEFONE',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone do Contabilista'
    )
    accountant_fax = models.CharField(
        db_column='CONTABILISTA_FAX',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Fax do Contabilista'
    )
    accountant_email = models.CharField(
        db_column='CONTABILISTA_EMAIL',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='E-mail do Contabilista'
    )
    accountant_code_municipality = models.ForeignKey(
        'locations.Municipality',
        models.DO_NOTHING,
        db_column='CONTABILISTA_CODIGO_MUNICIPIOS',
        related_name='filial_contabilista_codigo_municipios_set',
        blank=True,
        null=True,
        verbose_name='Código Município do Contabilista'
    )
    sped_ind_perfil = models.IntegerField(
        db_column='SPED_IND_PERFIL',
        blank=True,
        null=True,
        verbose_name='SPED Indicador de Perfil'
    )
    sped_ind_ativ = models.IntegerField(
        db_column='SPED_IND_ATIV',
        blank=True,
        null=True,
        verbose_name='SPED Indicador de Atividade'
    )
    code_bill_account = models.IntegerField(
        db_column='CODIGO_CONTA_BOLETO',
        blank=True,
        null=True,
        verbose_name='Código Conta Boleto'
    )
    sped_pc_ind_nat_pj = models.IntegerField(
        db_column='SPED_PC_IND_NAT_PJ',
        blank=True,
        null=True,
        verbose_name='SPED Indicador de Natureza Jurídica'
    )
    sped_pc_cod_inc_trib = models.IntegerField(
        db_column='SPED_PC_COD_INC_TRIB',
        blank=True,
        null=True,
        verbose_name='SPED Código de Incidência Tributária'
    )
    sped_pc_cod_tipo_cont = models.IntegerField(
        db_column='SPED_PC_COD_TIPO_CONT',
        blank=True,
        null=True,
        verbose_name='SPED Código de Tipo de Contabilidade'
    )
    sped_pc_ind_apro_cred = models.IntegerField(
        db_column='SPED_PC_IND_APRO_CRED',
        blank=True,
        null=True,
        verbose_name='SPED Indicador de Aprovação de Crédito'
    )
    sped_pc_ind_reg_cum = models.IntegerField(
        db_column='SPED_PC_IND_REG_CUM',
        blank=True,
        null=True,
        verbose_name='SPED Indicador de Registro Cumprido'
    )
    nfe_xml_authorized = models.CharField(
        db_column='NFE_XML_AUTORIZADO',
        max_length=400,
        blank=True,
        null=True,
        verbose_name='NFE XML Autorizado'
    )
    nfce_danfce = models.CharField(
        db_column='NFCE_DANFCE',
        max_length=300,
        blank=True,
        null=True,
        verbose_name='NFCe DANFCE'
    )
    nfce_csc = models.CharField(
        db_column='NFCE_CSC',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='NFCe CSC'
    )
    nfce_id_token = models.CharField(
        db_column='NFCE_ID_TOKEN',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='NFCe ID Token'
    )
    is_end_consumer_interstate_icms = models.IntegerField(
        db_column='CONSUMIDORFINAL_ICMSINTERESTATUAL',
        blank=True,
        null=True,
        verbose_name='É Consumidor Final ICMS Interestadual'
    )
    uses_cest = models.IntegerField(
        db_column='UTILIZA_CEST',
        blank=True,
        null=True,
        verbose_name='Utiliza CEST'
    )
    uses_calculus_inside = models.IntegerField(
        db_column='UTILIZA_CALCULO_POR_DENTRO',
        blank=True,
        null=True,
        verbose_name='Utiliza Cálculo por Dentro'
    )
    use_report_filter = models.IntegerField(
        db_column='UTILIZA_FILTRO_RELATORIO',
        blank=True,
        null=True,
        verbose_name='Utiliza Filtro de Relatório'
    )
    contract_holder = models.CharField(
        db_column='TITULAR_CONTRATO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Titular do Contrato'
    )
    cnpj_contract = models.CharField(
        db_column='CNPJ_CONTRATO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ do Contrato'
    )
    cpf_contract = models.CharField(
        db_column='CPF_CONTRATO',
        max_length=14,
        blank=True,
        null=True,
        verbose_name='CPF do Contrato'
    )
    aliquot_iss = models.DecimalField(
        db_column='ALIQUOTA_ISS',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Aliquota ISS'
    )
    use_cfs_grid_product = models.IntegerField(
        db_column='UTILIZA_CFS_GRID_PRODUTO',
        blank=True,
        null=True,
        verbose_name='Utiliza CFS Grid Produto'
    )
    uses_aliquot_by_region = models.IntegerField(
        db_column='UTILIZA_ALIQUOTA_POR_REGIAO',
        blank=True,
        null=True,
        verbose_name='Utiliza Alíquota por Região'
    )
    nfse_login = models.CharField(
        db_column='NFSE_LOGIN',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='NFSE Login'
    )
    nfse_password = models.CharField(
        db_column='NFSE_SENHA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='NFSE Senha'
    )
    uses_certificate = models.IntegerField(
        db_column='UTILIZA_CERTIFICADO',
        blank=True,
        null=True,
        verbose_name='Utiliza Certificado'
    )
    qrcode_side = models.IntegerField(
        db_column='QRCODE_LATERAL',
        blank=True,
        null=True,
        verbose_name='QRCode Lateral'
    )
    path_logo = models.CharField(
        db_column='CAMINHO_LOGO',
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Caminho da Logo'
    )
    integration_bases_wmw = models.CharField(
        db_column='BASE_INTEGRACAO_WMW',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Base de Integração WMW'
    )
    activation_code_sat = models.CharField(
        db_column='CODIGO_ATIVACAO_SAT',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Código de Ativação SAT'
    )
    signature_sat = models.CharField(
        db_column='ASSINATURA_SAT',
        max_length=350,
        blank=True,
        null=True,
        verbose_name='Assinatura SAT'
    )
    technical_manager_nfe = models.IntegerField(
        db_column='RESPONSAVEL_TECNICO_NFE',
        blank=True,
        null=True,
        verbose_name='Responsável Técnico NFE'
    )
    uses_date_filter_finan = models.IntegerField(
        db_column='UTILIZA_FILTRO_DATA_FINAN',
        blank=True,
        null=True,
        verbose_name='Utiliza Filtro de Data Financeiro'
    )
    uses_larger_obs_danfe = models.IntegerField(
        db_column='UTILIZA_OBS_MAIOR_DANFE',
        blank=True,
        null=True,
        verbose_name='Utiliza Observação Maior DANFE'
    )
    uses_partial_credit_card = models.IntegerField(
        db_column='UTILIZA_BAIXA_CREDITO_PARCIAL',
        blank=True,
        null=True,
        verbose_name='Utiliza Baixa de Crédito Parcial'
    )
    use_low_block_finan = models.IntegerField(
        db_column='UTILIZA_BLOQUEIO_BAIXA_FINAN',
        blank=True,
        null=True,
        verbose_name='Utiliza Bloqueio de Baixa Financeiro'
    )
    uses_annual_data_movements = models.IntegerField(
        db_column='UTILIZA_DATA_ANUAL_MOVIMENTACOES',
        blank=True,
        null=True,
        verbose_name='Utiliza Data Anual de Movimentações'
    )
    issuer_type_mdfe = models.IntegerField(
        db_column='TIPO_EMITENTE_MDFE',
        blank=True,
        null=True,
        verbose_name='Tipo de Emitente MDFE'
    )
    series_code_mdfe = models.IntegerField(
        db_column='CODIGO_SERIE_MDFE',
        blank=True,
        null=True,
        verbose_name='Código de Série MDFE'
    )
    mdfe_rntrc = models.CharField(
        db_column='MDFE_RNTRC',
        max_length=8,
        blank=True,
        null=True,
        verbose_name='MDFE RNTRC'
    )
    mdfe_damdfe = models.CharField(
        db_column='MDFE_DAMDFE',
        max_length=300,
        blank=True,
        null=True,
        verbose_name='MDFE DAMDFE'
    )
    status_api_payments = models.IntegerField(
        db_column='STATUS_API_PAGAMENTOS',
        blank=True,
        null=True,
        verbose_name='Status API Pagamentos'
    )
    code_account_api_payments = models.IntegerField(
        db_column='CODIGO_CONTA_API_PAGAMENTOS',
        blank=True,
        null=True,
        verbose_name='Código Conta API Pagamentos'
    )
    token_api_payments = models.CharField(
        db_column='TOKEN_API_PAGAMENTOS',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Token API Pagamentos'
    )
    send_proof_pay_email_api = models.IntegerField(
        db_column='ENVIA_COMPROVANTE_PAG_EMAIL_API',
        blank=True,
        null=True,
        verbose_name='Envia Comprovante de Pagamento por E-mail API'
    )
    id_api_connection_integration_nfe = models.CharField(
        db_column='ID_INTEGRACAO_API_CONEXAO_NFE',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='ID Integração API Conexão NFE'
    )
    user_api_blumetalk = models.CharField(
        db_column='USUARIO_API_BLUMETALK',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Usuario API Bluemetalk'
    )
    password_api_blumetalk = models.CharField(
        db_column='SENHA_API_BLUMETALK',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Senha API Bluemetalk'
    )
    nfse_cpf_user = models.CharField(
        db_column='NFSE_CPF_USUARIO',
        max_length=14,
        blank=True,
        null=True,
        verbose_name='NFSE CPF Usuário'
    )
    default_nfe_directory = models.CharField(
        db_column='DIRETORIO_PADRAO_NFE',
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Diretório Padrão NFE'
    )
    cnpj_payer_api_payment = models.CharField(
        db_column='CNPJ_PAGADOR_API_PAGAMENTO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ Pagador API Pagamento'
    )
    uses_history_product_search = models.IntegerField(
        db_column='UTILIZA_HIST_PESQUISA_PRODUTO',
        blank=True,
        null=True,
        verbose_name='Utiliza Histórico de Pesquisa de Produto'
    )
    use_confirmation_general_search = models.IntegerField(
        db_column='UTILIZA_CONFIRMARCAO_PESQUISA_GERAL',
        blank=True,
        null=True,
        verbose_name='Utiliza Confirmação de Pesquisa Geral'
    )
    uses_cliforn_global_standard = models.IntegerField(
        db_column='UTILIZA_CLIFORN_GLOBAL_PADRAO',
        blank=True,
        null=True,
        verbose_name='Utiliza Cliforn Global Padrão'
    )
    uses_global_default_product = models.IntegerField(
        db_column='UTILIZA_PRODUTO_GLOBAL_PADRAO',
        blank=True,
        null=True,
        verbose_name='Utiliza Produto Global Padrão'
    )

    class Meta:
        managed = False
        db_table = 'FILIAL'
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'

    def __str__(self):
        return self.fantasy_name if self.fantasy_name else f"Filial {self.code}"
