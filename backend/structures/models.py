from django.db import models


class Structure(models.Model):
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
        verbose_name='Código da Coligada (Ref)'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    type = models.IntegerField(
        db_column='TIPO',
        blank=True,
        null=True,
        verbose_name='Tipo'
    )  # Field name made lowercase.
    structure_id = models.CharField(
        db_column='IDESTRUTURA',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='ID da Estrutura'
    )  # Field name made lowercase.
    indirect_cost = models.DecimalField(
        db_column='CUSTOINDIRETO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Indireto'
    )  # Field name made lowercase.
    planned_structure_cost = models.DecimalField(
        db_column='CUSTOPREVISTOESTRUTURA',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Previsto da Estrutura'
    )  # Field name made lowercase.
    sequence = models.IntegerField(
        db_column='SEQUENCIA',
        blank=True,
        null=True,
        verbose_name='Sequência'
    )  # Field name made lowercase.
    image_address = models.CharField(
        db_column='ENDERECOIMAGEM',
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Endereço da Imagem'
    )  # Field name made lowercase.
    product_code = models.ForeignKey(
        'products.Product',  # Assuming 'product.Gproduto' translates to 'product.Product'
        models.DO_NOTHING,
        db_column='CODPRODUTO',
        blank=True,
        null=True,
        verbose_name='Produto'
    )  # Field name made lowercase.
    tech_data_multiple_quantity = models.DecimalField(
        db_column='DADOS_TEC_MULTIPLO_QTDE',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Dados Téc. Múltiplo Quantidade'
    )  # Field name made lowercase.
    tech_data_multiple_standard_width = models.DecimalField(
        db_column='DADOS_TEC_MULTIPLO_PADRAO_LARGURA',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Dados Téc. Múltiplo Padrão Largura'
    )  # Field name made lowercase.
    tech_data_multiple_standard_length = models.DecimalField(
        db_column='DADOS_TEC_MULTIPLO_PADRAO_COMPRIMENTO',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Dados Téc. Múltiplo Padrão Comprimento'
    )  # Field name made lowercase.
    gear_validation = models.IntegerField( # Engrenagem
        db_column='VALIDACAO_ENGRENAGEM',
        blank=True,
        null=True,
        verbose_name='Validação Engrenagem'
    )  # Field name made lowercase.
    wing_or_handle = models.IntegerField( # 'Asa' can mean wing or handle
        db_column='ASA',
        blank=True,
        null=True,
        verbose_name='Asa/Alça'
    )  # Field name made lowercase.
    z_factor = models.IntegerField( # Assuming Z is a factor or specific parameter
        db_column='Z',
        blank=True,
        null=True,
        verbose_name='Fator Z'
    )  # Field name made lowercase.
    revision1_flag = models.CharField( # 'revisao1' likely a flag or short code
        db_column='REVISAO1',
        max_length=1,
        blank=True,
        null=True,
        verbose_name='Revisão 1 (Flag)'
    )  # Field name made lowercase.
    parent_structure = models.ForeignKey(
        'self',
        models.DO_NOTHING,
        db_column='CODIGO_ESTRUTURA_PAI',
        blank=True,
        null=True,
        verbose_name='Estrutura Pai',
        related_name='child_structures'
    )  # Field name made lowercase.
    user_code = models.ForeignKey(
        'users_erp.Employee',
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        blank=True,
        null=True,
        verbose_name='Código do Usuário'
    )  # Field name made lowercase.
    revision_number = models.IntegerField( # Changed from 'revisao'
        db_column='REVISAO',
        blank=True,
        null=True,
        verbose_name='Revisão (Número)'
    )  # Field name made lowercase.
    is_main = models.IntegerField( # Changed from 'principal'
        db_column='PRINCIPAL',
        blank=True,
        null=True,
        verbose_name='Principal'
    )  # Field name made lowercase.
    creation_date = models.DateTimeField(
        db_column='DATA_CRIACAO',
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )  # Field name made lowercase.
    loss_percentage = models.DecimalField(
        db_column='PERCENTUAL_PERDA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Percentual de Perda'
    )  # Field name made lowercase.
    is_active_flag1 = models.IntegerField( # 'ativa' seems like an active flag
        db_column='ATIVA',
        blank=True,
        null=True,
        verbose_name='Ativa (Flag 1)'
    )  # Field name made lowercase.
    is_active_flag2 = models.IntegerField( # 'ativo' also seems like an active flag
        db_column='ATIVO',
        blank=True,
        null=True,
        verbose_name='Ativo (Flag 2)'
    )  # Field name made lowercase.
    observation = models.TextField(
        db_column='OBSERVACAO',
        blank=True,
        null=True,
        verbose_name='Observação'
    )  # Field name made lowercase. This field type is a guess.
    mrp_orders_balance = models.DecimalField(
        db_column='SALDO_ORDENS_MRP',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Saldo Ordens MRP'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_ESTRUTURA'
        verbose_name = 'Estrutura'
        verbose_name_plural = 'Estruturas'

    def __str__(self):
        return self.description if self.description else f"Estrutura {self.structure_id or self.code}"


class StructureActivity(models.Model):
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    activity_code = models.ForeignKey(
        'activitys.Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        verbose_name='Atividade'
    )  # Field name made lowercase.
    structure_code = models.ForeignKey(
        'Structure',  # Assuming 'FEstrutura' translates to 'Structure'
        models.DO_NOTHING,
        db_column='CODESTRUTURA',
        verbose_name='Estrutura',
        related_name='structure_activities'
    )  # Field name made lowercase.
    process_time = models.DecimalField(
        db_column='TEMPOPROCESSO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Tempo de Processo'
    )  # Field name made lowercase.
    process_type = models.IntegerField(
        db_column='TIPOPROCESSO',
        blank=True,
        null=True,
        verbose_name='Tipo de Processo'
    )  # Field name made lowercase.
    sequence = models.IntegerField(
        db_column='SEQUENCIA',
        blank=True,
        null=True,
        verbose_name='Sequência'
    )  # Field name made lowercase.
    workstation_code = models.ForeignKey(
        'workstation.Workstation',
        models.DO_NOTHING,
        db_column='CODPOSTO',
        blank=True,
        null=True,
        verbose_name='Código do Posto de Trabalho (Ref)'
    )  # Field name made lowercase.
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    cycle_time = models.DecimalField(
        db_column='TEMPOCICLO',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Tempo de Ciclo'
    )  # Field name made lowercase.
    cnc_program = models.CharField(
        db_column='PROGRAMACNC',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Programa CNC'
    )  # Field name made lowercase.
    preparation_notes = models.TextField( # Changed from 'preparacao'
        db_column='PREPARACAO',
        blank=True,
        null=True,
        verbose_name='Preparação (Notas)'
    )  # Field name made lowercase. This field type is a guess.
    execution_notes = models.TextField( # Changed from 'execucao'
        db_column='EXECUCAO',
        blank=True,
        null=True,
        verbose_name='Execução (Notas)'
    )  # Field name made lowercase. This field type is a guess.
    verification_notes = models.TextField( # Changed from 'conferencia'
        db_column='CONFERENCIA',
        blank=True,
        null=True,
        verbose_name='Conferência (Notas)'
    )  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'F_ATVESTRUTURA'
        verbose_name = 'Atividade da Estrutura'
        verbose_name_plural = 'Atividades da Estrutura'

    def __str__(self):
        return f"Atividade {self.activity_code_id} na Estrutura {self.structure_code_id} (Seq: {self.sequence})"