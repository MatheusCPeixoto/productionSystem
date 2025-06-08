from django.db import models


class Order(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',  # Assuming 'Coligada' translates to 'Company'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',  # Assuming 'Filial' translates to 'Branch'
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )  # Field name made lowercase.
    order_id = models.CharField(
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem'
    )  # Field name made lowercase.
    status = models.CharField(
        db_column='STATUS',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Status da Ordem'
    )  # Field name made lowercase.
    opening_date = models.DateTimeField(
        db_column='DATAABERTURA',
        blank=True,
        null=True,
        verbose_name='Data de Abertura'
    )  # Field name made lowercase.
    closing_date = models.DateTimeField(
        db_column='DATATERMINO',
        blank=True,
        null=True,
        verbose_name='Data de Término'
    )  # Field name made lowercase.
    necessity_origin = models.IntegerField(
        db_column='ORIGEMNECESSIDADE',
        blank=True,
        null=True,
        verbose_name='Origem da Necessidade'
    )  # Field name made lowercase.
    programming_type = models.IntegerField(
        db_column='TIPOPROGRAMACAO',
        blank=True,
        null=True,
        verbose_name='Tipo de Programação'
    )  # Field name made lowercase.
    order_description = models.CharField(
        db_column='DESCORDEM',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição da Ordem'
    )  # Field name made lowercase.
    responsible = models.CharField(
        db_column='RESPONSAVEL',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Responsável'
    )  # Field name made lowercase.
    order_type = models.IntegerField(
        db_column='TIPOORDEM',
        blank=True,
        null=True,
        verbose_name='Tipo de Ordem'
    )  # Field name made lowercase.
    order_observation = models.TextField(
        db_column='OBSORDEM',
        blank=True,
        null=True,
        verbose_name='Observação da Ordem'
    )  # Field name made lowercase. This field type is a guess.
    exp_mobile = models.CharField(
        db_column='EXPMOBILE',
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Exp. Mobile'
    )  # Field name made lowercase.
    order_cost = models.DecimalField(
        db_column='CUSTOORDEM',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Custo da Ordem'
    )  # Field name made lowercase.
    posted_quantity = models.DecimalField(
        db_column='QTDEAPONTADA',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Quantidade Apontada'
    )  # Field name made lowercase.
    planned_quantity = models.DecimalField(
        db_column='QTDEPREVISTA',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Quantidade Prevista'
    )  # Field name made lowercase.
    proportionality = models.DecimalField(
        db_column='PROPORCIONALIDADE',
        max_digits=20,
        decimal_places=10,
        verbose_name='Proporcionalidade'
    )  # Field name made lowercase.
    planning_code = models.IntegerField(
        db_column='CODIGO_PLANEJAMENTO',
        blank=True,
        null=True,
        verbose_name='Código do Planejamento'
    )  # Field name made lowercase.
    mrp_necessity_code = models.IntegerField(
        db_column='CODIGO_NECESSIDADEMRP',
        blank=True,
        null=True,
        verbose_name='Código da Necessidade MRP'
    )  # Field name made lowercase.
    order_printed = models.CharField(
        db_column='ORDEMIMPRESSA',
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Ordem Impressa'
    )  # Field name made lowercase.
    last_recalculation_date = models.DateTimeField(
        db_column='DATA_ULTIMO_RECALCULO',
        blank=True,
        null=True,
        verbose_name='Data do Último Recálculo'
    )  # Field name made lowercase.
    new_item_code = models.CharField(
        db_column='CODITEMNOVO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Código do Item Novo'
    )  # Field name made lowercase.
    brand = models.CharField(
        db_column='MARCA',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Marca'
    )  # Field name made lowercase.
    department = models.CharField(
        db_column='DEPARTAMENTO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Departamento'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_ORDEM'
        verbose_name = 'Ordem'
        verbose_name_plural = 'Ordens'

    def __str__(self):
        return self.order_id if self.order_id else f"Ordem {self.code}"


class OrderItem(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',  # Assuming 'Coligada' translates to 'Company'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )
    mrp_necessity = models.IntegerField(
        db_column='CODNECESSIDADE',
        blank=True,
        null=True,
        verbose_name='Necessidade MRP'
    )  # Field name made lowercase.
    order_id_fk = models.CharField(  # Renamed to avoid conflict with potential 'order' ForeignKey if FOrdem is also an 'Order' model
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem (Texto)'
    )  # Field name made lowercase.
    structure_code = models.ForeignKey(
        'structures.Structure',  # Assuming 'FEstrutura' translates to 'Structure'
        models.DO_NOTHING,
        db_column='CODESTRUTURA',
        blank=True,
        null=True,
        verbose_name='Código da Estrutura'
    )  # Field name made lowercase.
    necessity_date = models.DateTimeField(
        db_column='DTNECESSIDADE',
        blank=True,
        null=True,
        verbose_name='Data da Necessidade'
    )  # Field name made lowercase.
    planned_quantity = models.DecimalField(
        db_column='QUANTIDADEPREVISTA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Quantidade Prevista'
    )  # Field name made lowercase.
    completed_quantity = models.DecimalField(
        db_column='QUANTIDADEREALIZADA',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Quantidade Realizada'
    )  # Field name made lowercase.
    order_code = models.ForeignKey( # Assuming FOrdem was translated to Order
        'Order',
        models.DO_NOTHING,
        db_column='CODORDEM',
        blank=True,
        null=True,
        verbose_name='Ordem'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_ITEMORDEM'
        verbose_name = 'Item da Ordem'
        verbose_name_plural = 'Itens da Ordem'

    def __str__(self):
        return f"Item {self.code} da Ordem {self.order_code_id if self.order_code else self.order_id_fk}"


class OrderPlannedMaterial(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company = models.ForeignKey(
        'enterprises.Company',  # Assuming 'Coligada' translates to 'Company'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )  # Field name made lowercase.
    branch = models.ForeignKey(
        'enterprises.Branch',  # Assuming 'Filial' translates to 'Branch'
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )  # Field name made lowercase.
    order_code = models.ForeignKey(
        'Order',  # Assuming FOrdem translates to Order
        models.DO_NOTHING,
        db_column='CODORDEM',
        verbose_name='Ordem'
    )  # Field name made lowercase.
    order_id_text = models.CharField( # Renamed to distinguish from order ForeignKey
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem (Texto)'
    )  # Field name made lowercase.
    raw_material = models.ForeignKey(
        'products.Product',  # Assuming 'Gproduto' translates to 'Product'
        models.DO_NOTHING,
        db_column='CODMATPRIMA',
        blank=True,
        null=True,
        verbose_name='Matéria Prima'
    )  # Field name made lowercase.
    raw_material_id_text = models.CharField( # Renamed
        db_column='IDMATPRIMA',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID da Matéria Prima (Texto)'
    )  # Field name made lowercase.
    raw_material_description = models.CharField(
        db_column='DESCMATERIAPRIMA',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição da Matéria Prima'
    )  # Field name made lowercase.
    quantity = models.DecimalField(
        db_column='QUANTIDADE',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Quantidade'
    )  # Field name made lowercase.
    necessity_start_date = models.DateTimeField(
        db_column='DATAINICIONECESSIDADE',
        blank=True,
        null=True,
        verbose_name='Data de Início da Necessidade'
    )  # Field name made lowercase.
    planned_cost = models.DecimalField(
        db_column='CUSTOPREVISTO',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Custo Previsto'
    )  # Field name made lowercase.
    workstation_code = models.ForeignKey(
        'workstation.Workstation',
        models.DO_NOTHING,
        db_column='CODPOSTO',
        blank=True,
        null=True,
        verbose_name='Código do Posto de Trabalho'
    )  # Field name made lowercase.
    stock_location_code = models.IntegerField(
        db_column='CODLOCALESTOQUE',
        blank=True,
        null=True,
        verbose_name='Código do Local de Estoque'
    )  # Field name made lowercase.
    user = models.ForeignKey( # Assuming 'Colaborador' translates to 'Employee' or 'User'
        'users_erp.Employee', # Or 'User' if more appropriate
        models.DO_NOTHING,
        db_column='CODUSUARIO',
        blank=True,
        null=True,
        verbose_name='Usuário'
    )  # Field name made lowercase.
    activity = models.ForeignKey(
        'activitys.Activity',  # Assuming 'FAtividade' translates to 'Activity'
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade'
    )  # Field name made lowercase.
    sequence = models.IntegerField(
        db_column='SEQUENCIA',
        blank=True,
        null=True,
        verbose_name='Sequência'
    )  # Field name made lowercase.
    origin = models.IntegerField(
        db_column='ORIGEM',
        blank=True,
        null=True,
        verbose_name='Origem'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_MATERIALPREVISTOORDEM'
        verbose_name = 'Material Previsto da Ordem'
        verbose_name_plural = 'Materiais Previstos da Ordem'

    def __str__(self):
        return f"Material {self.raw_material_id_text or self.code} para Ordem {self.order_code_id}"