from django.db import models
import os


def get_product_file_path(instance, filename):
    """ Gera o caminho do arquivo, ex: products/PRD-001/images/desenho_vista_frontal.jpg """
    product_code = instance.product.code # Ou outro identificador único do produto
    file_type_folder = instance.get_file_type_display().lower().replace(' ', '_') # ex: 'desenho_tecnico'
    return os.path.join('products/media', str(product_code), file_type_folder, filename)


class Product(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    product_identifier = models.CharField(
        db_column='IDPRD',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='ID do Produto'
    )  # Field name made lowercase.
    name = models.CharField(
        db_column='NOME',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome'
    )  # Field name made lowercase.
    technical_description = models.CharField(
        db_column='DESCTECNICA',
        max_length=3000,
        blank=True,
        null=True,
        verbose_name='Descrição Técnica'
    )  # Field name made lowercase.
    creation_date = models.DateTimeField(
        db_column='DATACRIACAO',
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )  # Field name made lowercase.
    user_code = models.IntegerField(
        db_column='CODUSUARIO',
        blank=True,
        null=True,
        verbose_name='Código do Usuário'
    )  # Field name made lowercase.
    is_inactive = models.CharField(
        db_column='INATIVO',
        max_length=1,
        blank=True,
        null=True,
        verbose_name='Inativo'
    )  # Field name made lowercase.
    control_unit_code = models.IntegerField(
        db_column='CODUNDCONTROLE',
        blank=True,
        null=True,
        verbose_name='Código Unidade de Controle'
    )  # Field name made lowercase.
    purchase_unit_code = models.IntegerField(
        db_column='CODUNDCOMPRA',
        blank=True,
        null=True,
        verbose_name='Código Unidade de Compra'
    )  # Field name made lowercase.
    group_code = models.ForeignKey(
        'ProductGroup',
        models.DO_NOTHING,
        db_column='CODGRUPO',
        blank=True,
        null=True,
        verbose_name='Código do Grupo'
    )  # Field name made lowercase.
    subgroup_code = models.ForeignKey(
        'Subgroup',
        models.DO_NOTHING,
        db_column='CODSUBGRUPO',
        blank=True,
        null=True,
        verbose_name='Código do Subgrupo'
    )  # Field name made lowercase.
    free_field1 = models.CharField(
        db_column='CAMPOLIVRE1',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Campo Livre 1'
    )  # Field name made lowercase.
    free_field2 = models.CharField(
        db_column='CAMPOLIVRE2',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Campo Livre 2'
    )  # Field name made lowercase.
    free_field3 = models.CharField(
        db_column='CAMPOLIVRE3',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Campo Livre 3'
    )  # Field name made lowercase.
    free_date1 = models.DateTimeField(
        db_column='DATALIVRE1',
        blank=True,
        null=True,
        verbose_name='Data Livre 1'
    )  # Field name made lowercase.
    free_date2 = models.DateTimeField(
        db_column='DATALIVRE2',
        blank=True,
        null=True,
        verbose_name='Data Livre 2'
    )  # Field name made lowercase.
    free_date3 = models.DateTimeField(
        db_column='DATALIVRE3',
        blank=True,
        null=True,
        verbose_name='Data Livre 3'
    )  # Field name made lowercase.
    free_value1 = models.DecimalField(
        db_column='VALORLIVRE1',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Valor Livre 1'
    )  # Field name made lowercase.
    free_value2 = models.DecimalField(
        db_column='VALORLIVRE2',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Valor Livre 2'
    )  # Field name made lowercase.
    free_value3 = models.DecimalField(
        db_column='VALORLIVRE3',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Valor Livre 3'
    )  # Field name made lowercase.
    net_weight = models.DecimalField(
        db_column='PESOLIQUIDO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Peso Líquido'
    )  # Field name made lowercase.
    gross_weight = models.DecimalField(
        db_column='PESOBRUTO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Peso Bruto'
    )  # Field name made lowercase.
    minimum_stock = models.DecimalField(
        db_column='MINIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Mínimo em Estoque'
    )  # Field name made lowercase.
    maximum_stock = models.DecimalField(
        db_column='MAXIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Máximo em Estoque'
    )  # Field name made lowercase.
    reorder_point = models.DecimalField(
        db_column='PONTOPEDIDO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Ponto de Pedido'
    )  # Field name made lowercase.
    price1 = models.DecimalField(
        db_column='PRECO1',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Preço 1'
    )  # Field name made lowercase.
    price2 = models.DecimalField(
        db_column='PRECO2',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Preço 2'
    )  # Field name made lowercase.
    price3 = models.DecimalField(
        db_column='PRECO3',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Preço 3'
    )  # Field name made lowercase.
    average_cost = models.DecimalField(
        db_column='CUSTOMEDIO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Custo Médio'
    )  # Field name made lowercase.
    image_path = models.CharField(
        db_column='IMAGEM',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Imagem (Caminho)'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    length = models.DecimalField(
        db_column='COMPRIMENTO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Comprimento'
    )  # Field name made lowercase.
    width = models.DecimalField(
        db_column='LARGURA',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Largura'
    )  # Field name made lowercase.
    thickness = models.DecimalField(
        db_column='ESPESSURA',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Espessura'
    )  # Field name made lowercase.
    diameter = models.DecimalField(
        db_column='DIAMETRO',
        max_digits=14,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Diâmetro'
    )  # Field name made lowercase.
    validity_days = models.IntegerField(
        db_column='VALIDADEEMDIAS',
        blank=True,
        null=True,
        verbose_name='Validade em Dias'
    )  # Field name made lowercase.
    maximum_discount = models.DecimalField(
        db_column='DESCONTOMAXIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Desconto Máximo'
    )  # Field name made lowercase.
    commission1 = models.DecimalField(
        db_column='COMISSAO1',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Comissão 1'
    )  # Field name made lowercase.
    commission2 = models.DecimalField(
        db_column='COMISSAO2',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Comissão 2'
    )  # Field name made lowercase.
    commission3 = models.DecimalField(
        db_column='COMISSAO3',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Comissão 3'
    )  # Field name made lowercase.
    coloring_code = models.IntegerField(
        db_column='CODCOLORACAO',
        blank=True,
        null=True,
        verbose_name='Código Coloração'
    )  # Field name made lowercase.
    type = models.CharField(
        db_column='TIPO',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Tipo'
    )  # Field name made lowercase.
    manufacturer_component = models.CharField(
        db_column='COMPFAB',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Componente Fabricante'
    )  # Field name made lowercase.
    details = models.CharField(
        db_column='DETALHES',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Detalhes'
    )  # Field name made lowercase.
    brand = models.CharField(
        db_column='MARCA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Marca'
    )  # Field name made lowercase.
    size = models.CharField(
        db_column='tamanho',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Tamanho'
    )
    sale_price = models.DecimalField(
        db_column='PRECOVENDA',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Preço de Venda'
    )  # Field name made lowercase.
    parent_product_code = models.IntegerField(
        db_column='CODPRODUTOPAI',
        blank=True,
        null=True,
        verbose_name='Código do Produto Pai'
    )  # Field name made lowercase.
    weight_product_code1 = models.IntegerField(
        db_column='CODPRODUTOPESO1',
        blank=True,
        null=True,
        verbose_name='Código Produto Peso 1'
    )  # Field name made lowercase.
    weight_product_code2 = models.IntegerField(
        db_column='CODPRODUTOPESO2',
        blank=True,
        null=True,
        verbose_name='Código Produto Peso 2'
    )  # Field name made lowercase.
    change_parent_stock = models.DecimalField(
        db_column='ALTERARESTOQUEPAI',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Alterar Estoque Pai'
    )  # Field name made lowercase.
    parent_stock_change_type = models.CharField(
        db_column='TIPOALTERACAOESTOQUEPAI',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Tipo Alteração Estoque Pai'
    )  # Field name made lowercase.
    lead_time = models.IntegerField(
        db_column='LEADTIME',
        blank=True,
        null=True,
        verbose_name='Lead Time'
    )  # Field name made lowercase.
    analysis_time1 = models.IntegerField(
        db_column='TEMPOANALISE1',
        blank=True,
        null=True,
        verbose_name='Tempo Análise 1'
    )  # Field name made lowercase.
    analysis_time2 = models.IntegerField(
        db_column='TEMPOANALISE2',
        blank=True,
        null=True,
        verbose_name='Tempo Análise 2'
    )  # Field name made lowercase.
    rm_user_code = models.CharField(
        db_column='CODUSUARIO_RM',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Usuário RM'
    )  # Field name made lowercase.
    control_unit_symbol = models.CharField(
        db_column='SIMBOLO_UNDCONTROLE',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Símbolo Unidade Controle'
    )  # Field name made lowercase.
    purchase_unit_symbol = models.CharField(
        db_column='SIMBOLO_UNDCOMPRA',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Símbolo Unidade Compra'
    )  # Field name made lowercase.
    sale_unit_symbol = models.CharField(
        db_column='SIMBOLO_UNDVENDA',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Símbolo Unidade Venda'
    )  # Field name made lowercase.
    sale_unit_code = models.IntegerField(
        db_column='CODUNDVENDA',
        blank=True,
        null=True,
        verbose_name='Código Unidade Venda'
    )  # Field name made lowercase.
    rm_product_code = models.CharField(
        db_column='CODIGOPRD_RM',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Produto RM'
    )  # Field name made lowercase.
    rm_product_id = models.IntegerField(
        db_column='IDPRD_RM',
        blank=True,
        null=True,
        verbose_name='ID Produto RM'
    )  # Field name made lowercase.
    uses_batch = models.CharField(
        db_column='UTILIZALOTE',
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Utiliza Lote'
    )  # Field name made lowercase.
    height = models.DecimalField(
        db_column='ALTURA',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Altura'
    )  # Field name made lowercase.
    family_code1 = models.ForeignKey(
        'ProductFamily1',
        models.DO_NOTHING,
        db_column='CODFAMILIA1',
        blank=True,
        null=True,
        verbose_name='Código Família 1'
    )  # Field name made lowercase.
    family_code2 = models.ForeignKey(
        'ProductFamily2',
        models.DO_NOTHING,
        db_column='CODFAMILIA2',
        blank=True,
        null=True,
        verbose_name='Código Família 2'
    )  # Field name made lowercase.
    ncm_reference = models.CharField(
        db_column='REFERENCIA_NCM',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Referência NCM'
    )  # Field name made lowercase.
    ncm_number = models.IntegerField(
        db_column='NUMERO_NCM',
        blank=True,
        null=True,
        verbose_name='Número NCM'
    )  # Field name made lowercase.
    ncm_code = models.IntegerField(
        db_column='CODIGO_NCM',
        blank=True,
        null=True,
        verbose_name='Código NCM'
    )  # Field name made lowercase.
    origin = models.IntegerField(
        db_column='PROCEDENCIA',
        blank=True,
        null=True,
        verbose_name='Procedência'
    )  # Field name made lowercase.
    tax_classification = models.IntegerField(
        db_column='CLASSIFICACAOFISCAL',
        blank=True,
        null=True,
        verbose_name='Classificação Fiscal'
    )  # Field name made lowercase.
    commercial_item = models.CharField(
        db_column='ITEMCOMERCIAL',
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Item Comercial'
    )  # Field name made lowercase.
    old_system_code = models.CharField(
        db_column='CodSisAntigo',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Código Sistema Antigo'
    )  # Field name made lowercase.
    auxiliary_code = models.CharField(
        db_column='CODIGOAUXILIAR',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Auxiliar'
    )  # Field name made lowercase.
    minimum_sale_batch = models.DecimalField(
        db_column='LOTE_MINIMO_VENDA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Lote Mínimo Venda'
    )  # Field name made lowercase.
    multiple_sale_batch = models.DecimalField(
        db_column='LOTE_MULTIPLO_VENDA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Lote Múltiplo Venda'
    )  # Field name made lowercase.
    third_party_plate1 = models.TextField(
        db_column='PLACA_EM_TERCEIRO_1',
        blank=True,
        null=True,
        verbose_name='Placa em Terceiro 1'
    )  # Field name made lowercase. This field type is a guess.
    third_party_plate2 = models.TextField(
        db_column='PLACA_EM_TERCEIRO_2',
        blank=True,
        null=True,
        verbose_name='Placa em Terceiro 2'
    )  # Field name made lowercase. This field type is a guess.
    stock_address1 = models.CharField(
        db_column='ENDERECO_ESTOQUE1',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Endereço Estoque 1'
    )  # Field name made lowercase.
    shelf_division1 = models.CharField(
        db_column='DIVISAO_PRATELEIRA1',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Divisão Prateleira 1'
    )  # Field name made lowercase.
    shelf_number1 = models.CharField(
        db_column='NUMERO_PRATELEIRA1',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número Prateleira 1'
    )  # Field name made lowercase.
    stock_address2 = models.CharField(
        db_column='ENDERECO_ESTOQUE2',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Endereço Estoque 2'
    )  # Field name made lowercase.
    shelf_division2 = models.CharField(
        db_column='DIVISAO_PRATELEIRA2',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Divisão Prateleira 2'
    )  # Field name made lowercase.
    shelf_number2 = models.CharField(
        db_column='NUMERO_PRATELEIRA2',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número Prateleira 2'
    )  # Field name made lowercase.
    stock_address3 = models.CharField(
        db_column='ENDERECO_ESTOQUE3',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Endereço Estoque 3'
    )  # Field name made lowercase.
    shelf_division3 = models.CharField(
        db_column='DIVISAO_PRATELEIRA3',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Divisão Prateleira 3'
    )  # Field name made lowercase.
    shelf_number3 = models.CharField(
        db_column='NUMERO_PRATELEIRA3',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número Prateleira 3'
    )  # Field name made lowercase.
    dtec_mov_flat_length = models.DecimalField(
        db_column='DTEC_MOV_PLANOS_COMPRIMENTO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. Planos Comprimento'
    )  # Field name made lowercase.
    dtec_mov_flat_width = models.DecimalField(
        db_column='DTEC_MOV_PLANOS_LARGURA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. Planos Largura'
    )  # Field name made lowercase.
    dtec_mov_flat_thickness = models.DecimalField(
        db_column='DTEC_MOV_PLANOS_ESPESSURA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. Planos Espessura'
    )  # Field name made lowercase.
    dtec_mov_nonflat_solid_diameter = models.DecimalField(
        db_column='DTEC_MOV_NPLANOS_DMACICO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. NPlanos D. Maciço'
    )  # Field name made lowercase.
    dtec_mov_nonflat_internal_diameter = models.DecimalField(
        db_column='DTEC_MOV_NPLANOS_DINTERNO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. NPlanos D. Interno'
    )  # Field name made lowercase.
    dtec_mov_nonflat_external_diameter = models.DecimalField(
        db_column='DTEC_MOV_NPLANOS_DEXTERNO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. NPlanos D. Externo'
    )  # Field name made lowercase.
    dtec_mov_nonflat_length = models.DecimalField(
        db_column='DTEC_MOV_NPLANOS_COMPRIMENTO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. NPlanos Comprimento'
    )  # Field name made lowercase.
    dtec_mov_theoretical_weight = models.DecimalField(
        db_column='DTEC_MOV_PTEORICO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='DTEC Mov. Peso Teórico'
    )  # Field name made lowercase.
    merchandise_origin = models.IntegerField(
        db_column='ORIGEM_MERCADORIA',
        blank=True,
        null=True,
        verbose_name='Origem da Mercadoria'
    )  # Field name made lowercase.
    tax_classification_code_fk = models.IntegerField( # Suffix to avoid clash
        db_column='CODIGO_CLASSIFICACAOFISCAL',
        blank=True,
        null=True,
        verbose_name='Código Classificação Fiscal (Ref)'
    )  # Field name made lowercase.
    arbitrated_cost = models.DecimalField(
        db_column='CUSTO_ARBITRADO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Custo Arbitrado'
    )  # Field name made lowercase.
    composite_product = models.IntegerField(
        db_column='PRODUTOCOMPOSTO',
        blank=True,
        null=True,
        verbose_name='Produto Composto'
    )  # Field name made lowercase.
    mrp_stock = models.DecimalField(
        db_column='ESTOQUE_MRP',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Estoque MRP'
    )  # Field name made lowercase.
    cf_profit_margin = models.CharField(
        db_column='CF_MARGEMLL',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='CF Margem LL'
    )  # Field name made lowercase.
    cf_product_observation = models.CharField(
        db_column='CF_OBSERVACAO_PRD',
        max_length=8000,
        blank=True,
        null=True,
        verbose_name='CF Observação Produto'
    )  # Field name made lowercase.
    ipi_tax_situation = models.CharField(
        db_column='SITUACAO_TRIBUTARIA_IPI',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Situação Tributária IPI'
    )  # Field name made lowercase.
    cf_minimum_price = models.CharField(
        db_column='CF_PRECOMINIMO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='CF Preço Mínimo'
    )  # Field name made lowercase.
    uses_nfe_batch = models.CharField(
        db_column='UTILIZA_LOTE_NFE',
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Utiliza Lote NFe'
    )  # Field name made lowercase.
    anp_code = models.CharField( # ANP = Agência Nacional do Petróleo
        db_column='CODIGO_ANP',
        max_length=9,
        blank=True,
        null=True,
        verbose_name='Código ANP'
    )  # Field name made lowercase.
    anp_description = models.CharField(
        db_column='DESCRICAO_ANP',
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Descrição ANP'
    )  # Field name made lowercase.
    no_stock_control = models.IntegerField(
        db_column='NAO_CONTROLA_ESTOQUE',
        blank=True,
        null=True,
        verbose_name='Não Controla Estoque'
    )  # Field name made lowercase.
    gpl_percentage = models.DecimalField( # GPL = Gás Liquefeito de Petróleo
        db_column='PERCENTUAL_GPL',
        max_digits=22,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Percentual GPL'
    )  # Field name made lowercase.
    glgnn_percentage = models.DecimalField( # GLGNn = Gás Liquefeito de Gás Natural Nacional
        db_column='PERCENTUAL_GLGNN',
        max_digits=22,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Percentual GLGNn'
    )  # Field name made lowercase.
    glgni_percentage = models.DecimalField( # GLGNi = Gás Liquefeito de Gás Natural Importado
        db_column='PERCENTUAL_GLGNI',
        max_digits=22,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Percentual GLGNi'
    )  # Field name made lowercase.
    starting_value = models.DecimalField( # Valor de partida
        db_column='VALOR_PARTIDA',
        max_digits=14,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Valor de Partida'
    )  # Field name made lowercase.
    family_code3 = models.ForeignKey(
        'ProductFamily3',
        models.DO_NOTHING,
        db_column='CODFAMILIA3',
        blank=True,
        null=True,
        verbose_name='Código Família 3'
    )  # Field name made lowercase.
    family_code4 = models.ForeignKey(
        'ProductFamily4',
        models.DO_NOTHING,
        db_column='CODFAMILIA4',
        blank=True,
        null=True,
        verbose_name='Código Família 4'
    )  # Field name made lowercase.
    family_code5 = models.ForeignKey(
        'ProductFamily5',
        models.DO_NOTHING,
        db_column='CODFAMILIA5',
        blank=True,
        null=True,
        verbose_name='Código Família 5'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GPRODUTO'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name if self.name else f"Produto {self.code}"
    is_configurable = models.IntegerField(
        db_column='CONFIGURAVEL',
        blank=True,
        null=True,
        verbose_name='Configurável'
    )  # Field name made lowercase.
    is_kanban = models.IntegerField(
        db_column='KANBAN',
        blank=True,
        null=True,
        verbose_name='Kanban'
    )  # Field name made lowercase.
    log_timestamp = models.DateTimeField(
        db_column='LOG_DATA_HORA',
        blank=True,
        null=True,
        verbose_name='Log Data/Hora'
    )  # Field name made lowercase.
    sped_item_type_code = models.IntegerField(
        db_column='CODIGO_SPED_TIPO_ITEM',
        blank=True,
        null=True,
        verbose_name='Código Tipo Item SPED'
    )  # Field name made lowercase.
    sped_item_type_id = models.CharField(
        db_column='ID_SPED_TIPO_ITEM',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='ID Tipo Item SPED'
    )  # Field name made lowercase.
    sped_generic_code_code = models.IntegerField(
        db_column='CODIGO_SPED_COD_GEN',
        blank=True,
        null=True,
        verbose_name='Código Genérico SPED (Cod)'
    )  # Field name made lowercase.
    sped_generic_code_id = models.CharField(
        db_column='ID_SPED_COD_GEN',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='ID Genérico SPED (ID)'
    )  # Field name made lowercase.
    sped_lst_code_code = models.IntegerField(
        db_column='CODIGO_SPED_COD_LST',
        blank=True,
        null=True,
        verbose_name='Código LST SPED (Cod)'
    )  # Field name made lowercase.
    sped_lst_code_id = models.CharField(
        db_column='ID_SPED_COD_LST',
        max_length=4,
        blank=True,
        null=True,
        verbose_name='ID LST SPED (ID)'
    )  # Field name made lowercase.
    color_code = models.IntegerField(
        db_column='CODIGO_COR',
        blank=True,
        null=True,
        verbose_name='Código da Cor'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    minimum_selling_price = models.DecimalField(
        db_column='PRECO_VENDA_MINIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Preço de Venda Mínimo'
    )  # Field name made lowercase.
    framing_code = models.IntegerField( # Enquadramento
        db_column='CODIGO_ENQUADRAMENTO',
        blank=True,
        null=True,
        verbose_name='Código de Enquadramento'
    )  # Field name made lowercase.
    guideline_conversion_factor = models.DecimalField( # Fator de conversão pauta
        db_column='FATOR_CONVERSAO_PAUTA',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Fator de Conversão Pauta'
    )  # Field name made lowercase.
    ipi_entry_tax_situation = models.CharField(
        db_column='SITUACAO_TRIBUTARIA_IPI_ENTRADA',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Situação Tributária IPI Entrada'
    )  # Field name made lowercase.
    entry_framing_code = models.IntegerField( # Enquadramento entrada
        db_column='CODIGO_ENQUADRAMENTO_ENTRADA',
        blank=True,
        null=True,
        verbose_name='Código de Enquadramento Entrada'
    )  # Field name made lowercase.
    free_value4 = models.DecimalField(
        db_column='VALORLIVRE4',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Valor Livre 4'
    )  # Field name made lowercase.
    free_value5 = models.DecimalField(
        db_column='VALORLIVRE5',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Valor Livre 5'
    )  # Field name made lowercase.
    free_date4 = models.DateTimeField(
        db_column='DATALIVRE4',
        blank=True,
        null=True,
        verbose_name='Data Livre 4'
    )  # Field name made lowercase.
    free_date5 = models.DateTimeField(
        db_column='DATALIVRE5',
        blank=True,
        null=True,
        verbose_name='Data Livre 5'
    )  # Field name made lowercase.
    free_field4 = models.CharField(
        db_column='CAMPOLIVRE4',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Campo Livre 4'
    )  # Field name made lowercase.
    free_field5 = models.CharField(
        db_column='CAMPOLIVRE5',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Campo Livre 5'
    )  # Field name made lowercase.
    ean = models.CharField(
        db_column='EAN',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='EAN'
    )  # Field name made lowercase.
    taxable_ean = models.CharField(
        db_column='EAN_TRIBUTAVEL',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='EAN Tributável'
    )  # Field name made lowercase.
    ignore_inventory = models.CharField(
        db_column='NAO_CONSIDERAR_INVENTARIO',
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Não Considerar Inventário'
    )  # Field name made lowercase.
    fci_number = models.CharField( # FCI = Ficha de Conteúdo de Importação
        db_column='NUMERO_FCI',
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Número FCI'
    )  # Field name made lowercase.
    relevant_scale_indicator = models.CharField(
        db_column='INDICADOR_ESCALA_RELEVANTE',
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Indicador de Escala Relevante'
    )  # Field name made lowercase.
    manufacturer_cnpj = models.CharField(
        db_column='CNPJ_FABRICANTE',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ Fabricante'
    )  # Field name made lowercase.
    tax_benefit_code = models.CharField(
        db_column='CODIGO_BENEFICIO_FISCAL',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Código Benefício Fiscal'
    )  # Field name made lowercase.


class ProductCode(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    product = models.ForeignKey(
        'Product',  # Assuming 'Gproduto' translates to 'Product'
        models.DO_NOTHING,
        db_column='CODPRODUTO',
        verbose_name='Produto',
        related_name='similar_codes'
    )  # Field name made lowercase.
    similar_code = models.CharField(
        db_column='CODSIMILAR',
        max_length=50,
        verbose_name='Código Similar'
    )  # Field name made lowercase.
    company_code = models.IntegerField(
        db_column='CODCOLIGADA',
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    generation_date = models.DateTimeField(
        db_column='DATAGERAÇAO', # Note: 'DATAGERAÇAO' has 'Ç', ensure DB compatibility or rename
        verbose_name='Data de Geração'
    )  # Field name made lowercase.
    sale_price = models.DecimalField(
        db_column='PRECOVENDA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Preço de Venda'
    )  # Field name made lowercase.
    family1_code = models.IntegerField(
        db_column='CODIGO_FAMILIA1',
        blank=True,
        null=True,
        verbose_name='Código da Família 1'
    )  # Field name made lowercase.
    family1_description = models.CharField(
        db_column='DESCRICAO_FAMILIA1',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição da Família 1'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GPRODUTO_CODIGOS'
        verbose_name = 'Código de Produto'
        verbose_name_plural = 'Códigos de Produtos'
        unique_together = (('product', 'similar_code', 'company_code'),) # Suggested unique_together

    def __str__(self):
        return f"Código {self.similar_code} para Produto {self.product_id}"


class ProductBranch(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        verbose_name='Código da Filial'
    )  # Field name made lowercase.
    product_code = models.ForeignKey(
        'products.Product',  # Assuming 'product.Gproduto' translates to 'product.Product'
        models.DO_NOTHING,
        db_column='CODIGO_PRODUTO',
        verbose_name='Produto'
    )  # Field name made lowercase.
    balance = models.DecimalField(
        db_column='SALDO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Saldo'
    )  # Field name made lowercase.
    financial_balance = models.DecimalField(
        db_column='SALDO_FINANCEIRO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Saldo Financeiro'
    )  # Field name made lowercase.
    customer_balance = models.DecimalField(
        db_column='SALDO_CLIENTE',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Saldo Cliente'
    )  # Field name made lowercase.
    supplier_balance = models.DecimalField(
        db_column='SALDO_FORNECEDOR',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Saldo Fornecedor'
    )  # Field name made lowercase.
    average_cost = models.DecimalField(
        db_column='CUSTO_MEDIO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Custo Médio'
    )  # Field name made lowercase.
    last_purchase_cost = models.DecimalField(
        db_column='CUSTO_ULTIMA_COMPRA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Custo da Última Compra'
    )  # Field name made lowercase.
    minimum_stock = models.DecimalField(
        db_column='MINIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Mínimo em Estoque'
    )  # Field name made lowercase.
    maximum_stock = models.DecimalField(
        db_column='MAXIMO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Máximo em Estoque'
    )  # Field name made lowercase.
    reorder_point = models.DecimalField(
        db_column='PONTO_PEDIDO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Ponto de Pedido'
    )  # Field name made lowercase.
    supply_lead_time = models.DecimalField(
        db_column='LT_FORNECIMENTO',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Lead Time de Fornecimento'
    )  # Field name made lowercase.
    purchasing_lead_time = models.DecimalField(
        db_column='LT_COMPRAS',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Lead Time de Compras'
    )  # Field name made lowercase.
    transport_lead_time = models.DecimalField(
        db_column='LT_TRANSPORTE',
        max_digits=14,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Lead Time de Transporte'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GPRODUTO_FILIAL'
        verbose_name = 'Produto por Filial'
        verbose_name_plural = 'Produtos por Filial'

    def __str__(self):
        return f"Produto {self.product_code_id} na Filial {self.branch_code}"


class ProductGroup(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    group_id = models.CharField(
        db_column='IDGRUPO',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='ID do Grupo'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    cost_center_code = models.IntegerField( # Assuming CODCCUSTO refers to Cost Center Code
        db_column='CODCCUSTO',
        blank=True,
        null=True,
        verbose_name='Código do Centro de Custo'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )
    ignore_inventory = models.IntegerField(
        db_column='NAO_CONSIDERAR_INVENTARIO',
        blank=True,
        null=True,
        verbose_name='Não Considerar Inventário'
    )  # Field name made lowercase.
    cf_test = models.CharField( # Custom field, keeping 'cf' prefix if it's a convention
        db_column='CF_TESTE',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='CF Teste'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GRUPOPRODUTO'
        verbose_name = 'Grupo de Produto'
        verbose_name_plural = 'Grupos de Produtos'

    def __str__(self):
        return self.description if self.description else f"Grupo {self.group_id or self.code}"


class Subgroup(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    subgroup_id = models.CharField(
        db_column='IDSUBGRUPO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='ID do Subgrupo'
    )  # Field name made lowercase.
    cost_center_code = models.IntegerField(
        db_column='CODCCUSTO',
        blank=True,
        null=True,
        verbose_name='Código do Centro de Custo'
    )  # Field name made lowercase.
    group_code = models.ForeignKey(
        'ProductGroup',
        models.DO_NOTHING,
        db_column='CODGRUPO',
        blank=True,
        null=True,
        verbose_name='Código do Grupo (Ref)'
    )  # Field name made lowercase.
    credit = models.IntegerField(
        db_column='CREDITO',
        blank=True,
        null=True,
        verbose_name='Crédito'
    )  # Field name made lowercase.
    chart_of_accounts_code = models.IntegerField( # Plano de Contas
        db_column='CODPLANOCONTAS',
        blank=True,
        null=True,
        verbose_name='Código do Plano de Contas'
    )  # Field name made lowercase.
    field_a = models.IntegerField( # Assuming 'campoa' is a generic field
        db_column='CAMPOA',
        blank=True,
        null=True,
        verbose_name='Campo A'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'SUBGRUPO'
        verbose_name = 'Subgrupo'
        verbose_name_plural = 'Subgrupos'

    def __str__(self):
        return self.description if self.description else f"Subgrupo {self.subgroup_id or self.code}"


class ProductFamily1(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    family1_id = models.CharField(
        db_column='IDFAMILIA1',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='ID Família 1'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    cf_fixed_cost = models.CharField( # Custom field, keeping 'cf' prefix
        db_column='CF_CUSTOFIXO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='CF Custo Fixo'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'S_FAMILIA1'
        verbose_name = 'Família de Produto 1'
        verbose_name_plural = 'Famílias de Produto 1'

    def __str__(self):
        return self.description if self.description else f"Família 1 ({self.family1_id or self.code})"


class ProductFamily2(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    family2_id = models.CharField(
        db_column='IDFAMILIA2',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='ID Família 2'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'S_FAMILIA2'
        verbose_name = 'Família de Produto 2'
        verbose_name_plural = 'Famílias de Produto 2'

    def __str__(self):
        return self.description if self.description else f"Família 2 ({self.family2_id or self.code})"


class ProductFamily3(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    family3_id = models.CharField(
        db_column='IDFAMILIA3',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='ID Família 3'
    )  # Field name made lowercase.
    description = models.CharField( # Field name changed from 'descricao_familia3' to 'description' for consistency
        db_column='DESCRICAO_FAMILIA3',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição' # Simplified verbose_name
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'S_FAMILIA3'
        verbose_name = 'Família de Produto 3'
        verbose_name_plural = 'Famílias de Produto 3'

    def __str__(self):
        return self.description if self.description else f"Família 3 ({self.family3_id or self.code})"


class ProductFamily4(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    family4_id = models.CharField(
        db_column='IDFAMILIA4',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='ID Família 4'
    )  # Field name made lowercase.
    description = models.CharField( # Field name changed from 'descricao_familia3' to 'description' for consistency
        db_column='DESCRICAO_FAMILIA4',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição' # Simplified verbose_name
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'S_FAMILIA4'
        verbose_name = 'Família de Produto 4'
        verbose_name_plural = 'Famílias de Produto 4'

    def __str__(self):
        return self.description if self.description else f"Família 4 ({self.family4_id or self.code})"


class ProductFamily5(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    family5_id = models.CharField(
        db_column='IDFAMILIA5',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='ID Família 5'
    )  # Field name made lowercase.
    description = models.CharField( # Field name changed from 'descricao_familia3' to 'description' for consistency
        db_column='DESCRICAO_FAMILIA5',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Descrição' # Simplified verbose_name
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    class Meta:
        managed = False
        db_table = 'S_FAMILIA5'
        verbose_name = 'Família de Produto 5'
        verbose_name_plural = 'Famílias de Produto 5'

    def __str__(self):
        return self.description if self.description else f"Família 5 ({self.family5_id or self.code})"


def get_product_file_path(instance, filename):
    """ Gera o caminho do arquivo, ex: products/PRD-001/images/desenho_vista_frontal.jpg """
    product_code = instance.product.code # Ou outro identificador único do produto
    file_type_folder = instance.get_file_type_display().lower().replace(' ', '_') # ex: 'desenho_tecnico'
    return os.path.join('products/media', str(product_code), file_type_folder, filename)


class ProductFile(models.Model):
    class FileType(models.TextChoices):
        IMAGE = 'IMAGE', 'Imagem'
        PDF = 'PDF', 'PDF'
        TECHNICAL_DRAWING = 'TECHNICAL_DRAWING', 'Desenho Técnico'
        STL = 'STL', 'Modelo 3D (.stl)'

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Produto'
    )

    name = models.CharField(
        max_length=150,
        verbose_name='Nome / Título do Arquivo'
    )

    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        verbose_name='Tipo de Arquivo'
    )

    file = models.FileField(
        upload_to=get_product_file_path,
        verbose_name='Arquivo'
    )

    activities = models.ManyToManyField(
        'activitys.Activity',  # Ajuste o caminho para seu modelo de Atividade
        blank=True,  # Permite que um arquivo não seja associado a nenhuma atividade (será para TODAS)
        verbose_name='Atividades Específicas',
        help_text='Selecione uma ou mais atividades. Se nenhuma for selecionada, este arquivo será válido para todas as atividades do produto.'
    )
    # --- FIM DO NOVO CAMPO ---

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Upload'
    )

    class Meta:
        verbose_name = 'Arquivo de Produto'
        verbose_name_plural = 'Arquivos de Produto'
        ordering = ['file_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_file_type_display()}) para {self.product.name}"

