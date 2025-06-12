from django.db import models


class OrderActivityProgress(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODIGO_COLIGADA',
        verbose_name='Código da Coligada'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODIGO_FILIAL',
        verbose_name='Código da Filial'
    )  # Field name made lowercase.
    order_code = models.ForeignKey(
        'orders.Order',  # Assuming 'order.FOrdem' translates to 'order.Order'
        models.DO_NOTHING,
        db_column='CODIGO_ORDEM',
        verbose_name='Ordem'
    )  # Field name made lowercase.
    activity = models.ForeignKey(
        'activitys.Activity', # Assuming 'activity.Activity' is already correctly named
        models.DO_NOTHING,
        db_column='CODIGO_ATIVIDADE',
        verbose_name='Atividade',
        related_name='activity_progress'
    )  # Field name made lowercase.
    sequence = models.IntegerField(
        db_column='SEQUENCIA',
        verbose_name='Sequência'
    )  # Field name made lowercase.
    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.
    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Data de Fim'
    )  # Field name made lowercase.
    quantity = models.DecimalField(
        db_column='QUANTIDADE',
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Quantidade'
    )  # Field name made lowercase.
    # --- ADICIONE ESTE CAMPO AO SEU MODELO ---
    STATUS_CHOICES = [
        ('Em Andamento', 'Em Andamento'),
        ('Parado', 'Parado'),
        ('Finalizado', 'Finalizado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Em Andamento', # Define o valor inicial padrão
        verbose_name="Status do Apontamento"
    )

    class Meta:
        managed = True
        db_table = 'A_ATIVIDADE'
        verbose_name = 'Atividade da Ordem'
        verbose_name_plural = 'Atividades da Ordem'

    def __str__(self):
        return f"Atividade {self.activity_id} da Ordem {self.order_code_id} (Seq: {self.sequence})"


class ActivityEquipmentLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    order_activity = models.ForeignKey(
        'OrderActivityProgress',  # Assuming 'AAtividade' translates to 'OrderActivity'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        verbose_name='Atividade da Ordem',
        related_name = 'equipment_logs'
    )  # Field name made lowercase.
    equipment_code = models.ForeignKey(
        'equipments.Equipment',  # Assuming 'equipment.FEquipamento' translates to 'equipment.Equipment'
        models.DO_NOTHING,
        db_column='CODIGO_EQUIPAMENTO',
        verbose_name='Equipamento',
    )  # Field name made lowercase.
    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.
    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Data de Fim'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'A_EQUIPAMENTO'
        verbose_name = 'Log de Equipamento da Atividade'
        verbose_name_plural = 'Logs de Equipamento da Atividade'

    def __str__(self):
        return f"Log {self.code}: Equip. {self.equipment_code_id} em Ativ. Ordem {self.order_activity_id}"


class ActivityWorkforceLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    order_activity = models.ForeignKey(
        'OrderActivityProgress',  # Assuming 'AAtividade' translates to 'OrderActivity'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        verbose_name='Atividade da Ordem',
        related_name='workforce_logs'
    )  # Field name made lowercase.
    workforce_code = models.ForeignKey(
        'workforces.Workforce',  # Assuming 'manpower.FMaoobra' translates to 'manpower.Manpower'
        models.DO_NOTHING,
        db_column='CODIGO_MAOOBRA',
        verbose_name='Mão de Obra'
    )  # Field name made lowercase.
    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.
    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Data de Fim'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'A_MAOOBRA'
        verbose_name = 'Log de Mão de Obra da Atividade'
        verbose_name_plural = 'Logs de Mão de Obra da Atividade'

    def __str__(self):
        return f"Log {self.code}: Mão de Obra {self.workforce_code_id} em Ativ. Ordem {self.order_activity_id}"


class ActivityNonConformanceLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    order_activity = models.ForeignKey(
        'OrderActivityProgress',  # Assuming 'AAtividade' translates to 'OrderActivity'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade da Ordem'
    )  # Field name made lowercase.
    non_conformance = models.ForeignKey(
        'non_conformities.NonConformance',  # Assuming 'nonCompliant.FNaoconformidades' translates to 'nonCompliant.NonConformance'
        models.DO_NOTHING,
        db_column='CODIGO_NAOCONFORMIDADES',
        blank=True,
        null=True,
        verbose_name='Não Conformidade'
    )  # Field name made lowercase.
    quantity = models.DecimalField(
        db_column='QUANTIDADE',
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name='Quantidade'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'A_NAOCONFORMIDADE'
        verbose_name = 'Log de Não Conformidade da Atividade'
        verbose_name_plural = 'Logs de Não Conformidade da Atividade'

    def __str__(self):
        return f"Log NC {self.code}: NC {self.non_conformance_id} em Ativ. Ordem {self.order_activity_id}"


class EquipmentStoppageLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    order_activity = models.ForeignKey(
        'OrderActivityProgress',  # Assuming 'AAtividade' translates to 'OrderActivity'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        verbose_name='Atividade da Ordem'
    )  # Field name made lowercase.
    equipment_code = models.ForeignKey(
        'equipments.Equipment',  # Assuming 'equipment.FEquipamento' translates to 'equipment.Equipment'
        models.DO_NOTHING,
        db_column='CODIGO_EQUIPAMENTO',
        verbose_name='Equipamento'
    )  # Field name made lowercase.
    stop_reason_code = models.ForeignKey(
        'stop_reasons.StopReason',  # Assuming 'stopReason.FRazoesparada' translates to 'stopReason.StopReason'
        models.DO_NOTHING,
        db_column='CODIGO_RAZAOPARADA',
        verbose_name='Razão da Parada'
    )  # Field name made lowercase.
    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.
    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Data de Fim'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'A_PARADA_EQUIPAMENTO'
        verbose_name = 'Log de Parada de Equipamento'
        verbose_name_plural = 'Logs de Parada de Equipamento'

    def __str__(self):
        return f"Parada {self.code}: Equip. {self.equipment_code_id} em Ativ. Ordem {self.order_activity_id} (Razão: {self.stop_reason_code_id})"


class WorkforceStoppageLog(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    order_activity = models.ForeignKey(
        'OrderActivityProgress',  # Assuming 'AAtividade' translates to 'OrderActivity'
        models.DO_NOTHING,
        db_column='CODIGO_APONTAMENTOATIVIDADE',
        verbose_name='Atividade da Ordem'
    )  # Field name made lowercase.
    workforce_code = models.ForeignKey(
        'workforces.Workforce',  # Assuming 'manpower.FMaoobra' translates to 'manpower.Manpower'
        models.DO_NOTHING,
        db_column='CODIGO_MAOOBRA',
        verbose_name='Mão de Obra'
    )  # Field name made lowercase.
    stop_reason_code = models.ForeignKey(
        'stop_reasons.StopReason',  # Assuming 'stopReason.FRazoesparada' translates to 'stopReason.StopReason'
        models.DO_NOTHING,
        db_column='CODIGO_RAZAOPARADA',
        verbose_name='Razão da Parada'
    )  # Field name made lowercase.
    start_date = models.DateTimeField(
        db_column='DATA_INICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.
    end_date = models.DateTimeField(
        db_column='DATA_FIM',
        blank=True,
        null=True,
        verbose_name='Data de Fim'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'A_PARADA_MAOOBRA'
        verbose_name = 'Log de Parada de Mão de Obra'
        verbose_name_plural = 'Logs de Parada de Mão de Obra'

    def __str__(self):
        return f"Parada {self.code}: M.O. {self.workforce_code_id} em Ativ. Ordem {self.order_activity_id} (Razão: {self.stop_reason_code_id})"
