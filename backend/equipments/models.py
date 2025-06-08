from django.db import models


class Equipment(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.IntegerField(
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    branch_code = models.IntegerField(
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCEQUIPAMENTO',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição do Equipamento'
    )  # Field name made lowercase.
    workstation_code = models.ForeignKey(
        'workstation.Workstation',  # Assuming FPostos will be translated to Workstation or similar
        models.DO_NOTHING,
        db_column='CODPOSTO',
        blank=True,
        null=True,
        verbose_name='Posto de Trabalho'
    )  # Field name made lowercase.
    hourly_cost = models.DecimalField(
        db_column='CUSTOHORAEQP',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Hora do Equipamento'
    )  # Field name made lowercase.
    cost_center_code = models.CharField(
        db_column='CODCCUSTO',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Código do Centro de Custo'
    )  # Field name made lowercase.
    monthly_cost = models.DecimalField(
        db_column='CUSTOMESEQP',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Mensal do Equipamento'
    )  # Field name made lowercase.
    effectiveness = models.DecimalField(
        db_column='EFETIVIDADE',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Efetividade'
    )  # Field name made lowercase.
    active_quantity = models.IntegerField(
        db_column='QTDATIVA',
        blank=True,
        null=True,
        verbose_name='Quantidade Ativa'
    )  # Field name made lowercase.
    hourly_production = models.DecimalField(
        db_column='PRODHORA',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Produção por Hora'
    )  # Field name made lowercase.
    equipment_id = models.CharField(
        db_column='IDEQUIPAMENTO',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID do Equipamento'
    )  # Field name made lowercase.
    address = models.CharField(
        db_column='ENDERECO',
        max_length=300,
        blank=True,
        null=True,
        verbose_name='Endereço'
    )  # Field name made lowercase.
    daily_efficiency = models.DecimalField(
        db_column='EFICIENCIADIA',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Eficiência Diária'
    )  # Field name made lowercase.
    monthly_efficiency = models.DecimalField(
        db_column='EFICIENCIAMES',
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name='Eficiência Mensal'
    )  # Field name made lowercase.
    type = models.IntegerField(
        db_column='TIPO',
        blank=True,
        null=True,
        verbose_name='Tipo'
    )  # Field name made lowercase.
    work_shift_minutes = models.IntegerField(
        db_column='TT_TURNO_TRAB_MINUTOS',
        blank=True,
        null=True,
        verbose_name='Total Turno de Trabalho (Minutos)'
    )  # Field name made lowercase.
    cost_sql = models.TextField(
        db_column='SQL_CUSTO',
        blank=True,
        null=True,
        verbose_name='SQL de Custo'
    )  # Field name made lowercase. This field type is a guess.
    equipment_observation = models.CharField(
        db_column='CF_OBSERVACAO_EQP',
        max_length=8000,
        blank=True,
        null=True,
        verbose_name='Observação do Equipamento'
    )  # Field name made lowercase.
    utility_notes = models.CharField(
        db_column='CF_UTILIDADE',
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Utilidade'
    )  # Field name made lowercase.
    usage_notes = models.CharField(
        db_column='CF_UTILIZACAO',
        max_length=300,
        blank=True,
        null=True,
        verbose_name='Utilização'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_EQUIPAMENTO'
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return self.description if self.description else f"Equipamento {self.code}"


class CompositeEquipment(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,  # Assuming this should be the primary key
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.IntegerField(
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    branch_code = models.IntegerField(
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )  # Field name made lowercase.
    parent_equipment_code = models.ForeignKey(
        'Equipment',  # Updated to assumed English name of FEquipamento
        models.DO_NOTHING,
        db_column='CODEQUIPAMENTOPAI',
        blank=True,
        null=True,
        verbose_name='Código do Equipamento Pai',
        related_name='child_composite_equipment' # Added a clear related_name
    )  # Field name made lowercase.
    child_equipment_code = models.ForeignKey(
        'Equipment',  # Updated to assumed English name of FEquipamento
        models.DO_NOTHING,
        db_column='CODEQUIPAMENTOFILHO',
        related_name='parent_composite_equipment', # Changed from default generated
        blank=True,
        null=True,
        verbose_name='Código do Equipamento Filho'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_EQUIPAMENTOCOMPOSTO'
        verbose_name = 'Equipamento Composto'
        verbose_name_plural = 'Equipamentos Compostos'
        unique_together = (('parent_equipment_code', 'child_equipment_code'),) # Added example unique_together

    def __str__(self):
        parent_id = self.parent_equipment_code_id if self.parent_equipment_code else 'N/A'
        child_id = self.child_equipment_code_id if self.child_equipment_code else 'N/A'
        return f"Composição {self.code}: Pai ({parent_id}) -> Filho ({child_id})"


class EquipmentSkill(models.Model):
    company_code = models.ForeignKey(
        'enterprises.Company',  # Assuming 'Coligada' translates to 'Company'
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Coligada'
    )  # Field name made lowercase.
    equipment_code = models.ForeignKey(
        'Equipment',  # Assuming 'FEquipamento' translates to 'Equipment'
        models.DO_NOTHING,
        db_column='CODEQUIPAMENTO',
        verbose_name='Equipamento'
    )  # Field name made lowercase.
    skill_code = models.ForeignKey(
        'workforces.Skill',  # Assuming 'FHabilidade' translates to 'Skill'
        models.DO_NOTHING,
        db_column='CODHABILIDADE',
        verbose_name='Habilidade'
    )  # Field name made lowercase.
    skill_quantity = models.IntegerField(
        db_column='QTDHABILIDADE',
        blank=True,
        null=True,
        verbose_name='Quantidade da Habilidade'
    )  # Field name made lowercase.
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_EQUIPAMENTOHABILIDADES'
        verbose_name = 'Habilidade do Equipamento'
        verbose_name_plural = 'Habilidades dos Equipamentos'
        unique_together = (('company_code', 'equipment_code', 'skill_code'),) # Suggested unique_together

    def __str__(self):
        return f"Habilidade {self.skill_code_id} para Equipamento {self.equipment_code_id} (Coligada: {self.company_code_id})"


class EquipmentCostHistory(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,  # Assuming this should be the primary key
        verbose_name='Código'
    )  # Field name made lowercase.
    equipment_code = models.ForeignKey(
        'Equipment',  # Assuming FEquipamento translates to Equipment
        models.DO_NOTHING,
        db_column='CODEQUIPAMENTO',
        blank=True,
        null=True,
        verbose_name='Equipamento'
    )  # Field name made lowercase.
    month = models.CharField(
        db_column='MES',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='Mês'
    )  # Field name made lowercase.
    year = models.CharField(
        db_column='ANO',
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Ano'
    )  # Field name made lowercase.
    hourly_cost = models.DecimalField(
        db_column='CUSTOHORA',
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Custo Hora'
    )  # Field name made lowercase.
    monthly_cost = models.DecimalField(
        db_column='CUSTOMES',
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Custo Mês'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
    )  # Field name made lowercase.
    is_current = models.IntegerField(
        db_column='ATUAL',
        blank=True,
        null=True,
        verbose_name='Atual'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_HISTCUSTOEQUIPAMENTO'
        verbose_name = 'Histórico de Custo do Equipamento'
        verbose_name_plural = 'Históricos de Custo dos Equipamentos'
        unique_together = (('equipment_code', 'month', 'year', 'company_code', 'branch_code'),) # Suggested unique_together

    def __str__(self):
        return f"Histórico {self.code} - Equip: {self.equipment_code_id} ({self.month}/{self.year})"