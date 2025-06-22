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


class Appointment(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )

    order_id_text = models.CharField(
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem (Texto)'
    )

    order_code = models.ForeignKey(
        'Order',  # Supondo que FOrdem seja o modelo Order no app 'orders'
        models.DO_NOTHING,
        db_column='CODORDEM',
        blank=True,
        null=True,
        verbose_name='Ordem'
    )

    parent_order_id = models.CharField(
        db_column='ORDEM_PAI',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Ordem Pai'
    )

    company_code = models.ForeignKey(
        'enterprises.Company',  # Supondo que Coligada seja Company no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )

    branch_code = models.ForeignKey(
        'enterprises.Branch',  # Supondo que Filial seja Branch no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )

    activity_code = models.ForeignKey(
        'activitys.Activity',  # Supondo que FAtividade seja Activity no app 'activitys'
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade'
    )

    workstation_code = models.ForeignKey(
        'workstation.Workstation',  # Supondo que FPostos seja Workstation no app 'workstation'
        models.DO_NOTHING,
        db_column='CODPOSTO',
        blank=True,
        null=True,
        verbose_name='Posto de Trabalho'
    )

    sequence = models.IntegerField(
        db_column='SEQUENCIA',
        blank=True,
        null=True,
        verbose_name='Sequência'
    )

    start_date = models.DateTimeField(
        db_column='INICIOEFETIVO',
        blank=True,
        null=True,
        verbose_name='Início Efetivo'
    )

    end_date = models.DateTimeField(
        db_column='FIMEFETIVO',
        blank=True,
        null=True,
        verbose_name='Fim Efetivo'
    )

    pointed_quantity = models.DecimalField(
        db_column='QTDEAPONTADA',
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Quantidade Apontada'
    )

    effective_cost = models.DecimalField(
        db_column='CUSTOEFETIVO',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Custo Efetivo'
    )

    integration_status = models.CharField(
        db_column='STATUSINTEGRACAO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Status de Integração'
    )

    material_status = models.CharField(  # statusmp traduzido para material_status
        db_column='STATUSMP',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Status Matéria-Prima'
    )

    user_code = models.ForeignKey(
        'users_erp.Employee',  # Supondo que Colaborador seja Employee no app 'users_erp'
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        blank=True,
        null=True,
        verbose_name='Usuário de Criação'
    )

    created_at = models.DateTimeField(
        db_column='DTCRIACAO',
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        managed = False
        db_table = 'F_APONTAMENTOATIVIDADE'
        verbose_name = 'Apontamento de Atividade'
        verbose_name_plural = 'Apontamentos de Atividade'

    def __str__(self):
        return f"Apontamento {self.code} para Ordem {self.order_id_text}"


class WorkforceAppointmentLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código do Log'
    )

    order_id_text = models.CharField(
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem (Texto)'
    )

    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )

    activity_code = models.ForeignKey(
        'activitys.Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade'
    )

    start_date = models.DateTimeField(
        db_column='INICIOEFETIVO',
        blank=True,
        null=True,
        verbose_name='Início Efetivo'
    )

    end_date = models.DateTimeField(
        db_column='FIMEFETIVO',
        blank=True,
        null=True,
        verbose_name='Fim Efetivo'
    )

    workforce_code = models.ForeignKey(
        'workforces.Workforce',  # Usando o padrão 'app_name.ModelName'
        models.DO_NOTHING,
        db_column='CODMAOOBRA',
        blank=True,
        null=True,
        verbose_name='Mão de Obra'
    )

    effective_cost = models.DecimalField(
        db_column='CUSTOEFETIVO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Efetivo'
    )

    pointed_quantity = models.DecimalField(
        db_column='QTDEAPONTADA',
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Quantidade Apontada'
    )

    branch_code = models.IntegerField(
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )

    # Relação com a Ordem (se for uma FK para um modelo 'Order')
    order_code = models.ForeignKey(
        'orders.Order',
        models.DO_NOTHING,
        db_column='CODORDEM',
        blank=True,
        null=True,
        verbose_name='Ordem'
    )

    # Relação com o apontamento principal
    activity_progress = models.ForeignKey(
        'Appointment',  # Ajuste app_name se necessário
        models.DO_NOTHING,
        db_column='CODAPONTAMENTOATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Apontamento da Atividade'
    )

    # Relação com o usuário/colaborador
    user_code = models.ForeignKey(
        'users_erp.Employee',  # Ou 'User', conforme seu modelo
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        blank=True,
        null=True,
        verbose_name='Usuário'
    )

    created_at = models.DateTimeField(
        db_column='DTCRIACAO',
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        managed = False
        db_table = 'F_APONTAMENTOMOBRA'
        verbose_name = 'Log de Apontamento de Mão de Obra'
        verbose_name_plural = 'Logs de Apontamento de Mão de Obra'

    def __str__(self):
        return f"Log {self.code} - Ordem {self.order_id_text} - Op. {self.workforce_code}"


class EquipmentAppointmentLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código do Log'
    )

    order_id_text = models.CharField(
        db_column='IDORDEM',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ID da Ordem (Texto)'
    )

    order_code = models.ForeignKey(
        'orders.Order',  # Supondo que FOrdem seja Order no app 'orders'
        models.DO_NOTHING,
        db_column='CODORDEM',
        blank=True,
        null=True,
        verbose_name='Ordem'
    )

    company_code = models.ForeignKey(
        'enterprises.Company',  # Supondo que Coligada seja Company no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )

    branch_code = models.ForeignKey(
        'enterprises.Branch',  # Supondo que Filial seja Branch no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )

    activity_code = models.ForeignKey(
        'activitys.Activity',  # Supondo que FAtividade seja Activity no app 'activitys'
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade'
    )

    # Relação com o apontamento principal
    activity_progress = models.ForeignKey(
        'Appointment',  # Usando o novo nome do modelo Appointment
        models.DO_NOTHING,
        db_column='CODAPONTAMENTOATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Apontamento da Atividade'
    )

    # Relação com o modelo de Equipamento
    equipment_code = models.ForeignKey(
        'equipments.Equipment',  # Supondo que o modelo seja Equipment no app 'equipments'
        models.DO_NOTHING,
        db_column='CODEQUIPAMENTO',
        blank=True,
        null=True,
        verbose_name='Equipamento'
    )

    start_date = models.DateTimeField(
        db_column='INICIOEFETIVO',
        blank=True,
        null=True,
        verbose_name='Início Efetivo'
    )

    end_date = models.DateTimeField(
        db_column='FIMEFETIVO',
        blank=True,
        null=True,
        verbose_name='Fim Efetivo'
    )

    pointed_quantity = models.DecimalField(
        db_column='QTDEAPONTADA',
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Quantidade Apontada'
    )

    effective_cost = models.DecimalField(
        db_column='CUSTOEFETIVO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Efetivo'
    )

    user_code = models.ForeignKey(
        'users_erp.Employee',  # Ou o nome do seu modelo de usuário/colaborador
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        blank=True,
        null=True,
        verbose_name='Usuário de Criação'
    )

    created_at = models.DateTimeField(
        db_column='DTCRIACAO',
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        managed = False
        db_table = 'F_APONTAMENTOEQUIPAMENTO'
        verbose_name = 'Log de Apontamento de Equipamento'
        verbose_name_plural = 'Logs de Apontamento de Equipamento'

    def __str__(self):
        return f"Log {self.code} - Ordem {self.order_id_text} - Equip. {self.equipment_code}"


class StoppageAppointmentEquipmentLog(models.Model):
    # O nome da classe foi traduzido para um nome claro em inglês.

    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código do Log de Parada'
    )

    company_code = models.ForeignKey(
        'enterprises.Company',  # Supondo que Coligada seja Company no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Coligada'
    )

    branch_code = models.ForeignKey(
        'enterprises.Branch',  # Supondo que Filial seja Branch no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )

    # Relação com o apontamento principal
    activity_progress = models.ForeignKey(
        'Appointment',  # Usando o nome refatorado 'Appointment'
        models.DO_NOTHING,
        db_column='CODAPONTAMENTOATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Apontamento da Atividade'
    )

    # Relação com o modelo de Equipamento
    equipment_code = models.ForeignKey(
        'equipments.Equipment',  # Supondo que FEquipamento seja Equipment no app 'equipments'
        models.DO_NOTHING,
        db_column='COEQUIPAMENTO',
        blank=True,
        null=True,
        verbose_name='Equipamento'
    )

    # Relação com o motivo da parada
    stop_reason_code = models.ForeignKey(
        'stop_reasons.StopReason',  # Supondo que FRazoesparada seja StopReason no app 'stop_reasons'
        models.DO_NOTHING,
        db_column='CODRAZAOPARADA',
        blank=True,
        null=True,
        verbose_name='Motivo da Parada'
    )

    start_date = models.DateTimeField(
        db_column='INICIOPARADA',
        blank=True,
        null=True,
        verbose_name='Início da Parada'
    )

    end_date = models.DateTimeField(
        db_column='FIMPARADA',
        blank=True,
        null=True,
        verbose_name='Fim da Parada'
    )

    user_code = models.ForeignKey(
        'users_erp.Employee',  # Ou o nome do seu modelo de usuário/colaborador
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        blank=True,
        null=True,
        verbose_name='Usuário de Criação'
    )

    created_at = models.DateTimeField(
        db_column='DTCRIACAO',
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        managed = False
        db_table = 'F_APONTAMENTOPARADAS'
        verbose_name = 'Log de Apontamento de Parada'
        verbose_name_plural = 'Logs de Apontamento de Parada'

    def __str__(self):
        return f"Parada {self.code} para Apontamento {self.activity_progress_id}"


class StoppageAppointmentWorkforceLog(models.Model):
    # O nome da classe foi traduzido para um nome claro em inglês.

    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código do Log de Parada'
    )

    company_code = models.ForeignKey(
        'enterprises.Company',  # Supondo que Coligada seja Company no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODIGO_COLIGADA',
        verbose_name='Coligada'
    )

    branch_code = models.ForeignKey(
        'enterprises.Branch',  # Supondo que Filial seja Branch no app 'enterprises'
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        verbose_name='Filial'
    )

    # Relação com o apontamento principal
    activity_progress = models.ForeignKey(
        'Appointment',  # Usando o nome refatorado 'Appointment'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        verbose_name='Apontamento da Atividade'
    )

    # Relação com a Mão de Obra que parou
    workforce_code = models.ForeignKey(
        'workforces.Workforce',  # Supondo que FMaoobra seja Workforce no app 'workforces'
        models.DO_NOTHING,
        db_column='CODIGO_MAOOBRA',
        verbose_name='Mão de Obra'
    )

    # Relação com o motivo da parada
    stop_reason_code = models.ForeignKey(
        'stop_reasons.StopReason',  # Supondo que FRazoesparada seja StopReason
        models.DO_NOTHING,
        db_column='CODIGO_RAZOESPARADA',
        verbose_name='Motivo da Parada'
    )

    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Início da Parada'
    )

    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Fim da Parada'
    )

    user_code = models.ForeignKey(
        'users_erp.Employee',  # Ou o nome do seu modelo de usuário/colaborador
        models.DO_NOTHING,
        db_column='CODIGO_USUARIO',
        verbose_name='Usuário de Criação'
    )

    created_at = models.DateTimeField(
        db_column='DTCRIACAO',
        blank=True,
        null=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        managed = False
        db_table = 'F_APONTAMENTOPARADAS_MAOOBRA'
        verbose_name = 'Log de Parada de Mão de Obra'
        verbose_name_plural = 'Logs de Parada de Mão de Obra'

    def __str__(self):
        return f"Parada do Op. {self.workforce_code_id} no Apontamento {self.activity_progress_id}"