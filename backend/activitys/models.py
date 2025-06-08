from django.db import models


class Activity(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Empresa'
    )
    branch_code = models.IntegerField(
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )
    description = models.CharField(
        db_column='DESCATIVIDADE',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    preparation = models.TextField(
        db_column='PREPARACAO',
        blank=True,
        null=True,
        verbose_name='Preparação'
    )
    execution = models.TextField(
        db_column='EXECUCAO',
        blank=True,
        null=True,
        verbose_name='Execução'
    )
    verification = models.TextField(
        db_column='CONFERENCIA',
        blank=True,
        null=True,
        verbose_name='Conferência'
    )
    activity_id = models.CharField(
        db_column='IDATIVIDADE',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID da Atividade'
    )
    setup = models.IntegerField(
        db_column='SETUP',
        blank=True,
        null=True,
        verbose_name='Setup'
    )
    is_active = models.IntegerField(
        db_column='ATIVO',
        blank=True,
        null=True,
        verbose_name='Ativo'
    )

    class Meta:
        managed = False
        db_table = 'F_ATIVIDADE'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return self.description if self.description else f"Atividade {self.code}"


class ActivitySetup(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )
    activity_code = models.ForeignKey(
        'Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        verbose_name='Atividade Principal'
    )
    activity_code_setup = models.ForeignKey(
        'Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADESETUP',
        related_name='fatividadesetup_codatividadesetup_set',
        verbose_name='Atividade de Setup'
    )

    class Meta:
        managed = False
        db_table = 'F_ATIVIDADE_SETUP'
        verbose_name = 'Setup de Atividade'
        verbose_name_plural = 'Setups de Atividades'

    def __str__(self):
        return f"Setup {self.code}: {self.activity_code} -> {self.activity_code_setup}"


class ActivityEquipment(models.Model):
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Empresa'
    )
    activity_code = models.ForeignKey(
        'Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        verbose_name='Atividade'
    )
    # codequipamento = models.ForeignKey(
    #     'FEquipamento',
    #     models.DO_NOTHING,
    #     db_column='CODEQUIPAMENTO',
    #     verbose_name='Código do Equipamento'
    # )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )

    class Meta:
        managed = False
        db_table = 'F_ATIVEQUIPAMENTO'
        verbose_name = 'Equipamento da Atividade'
        verbose_name_plural = 'Equipamentos da Atividade'

    def __str__(self):
        return f"Equipamento da Atividade {self.code} (Atividade: {self.activity_code_id})"


class ActivitySkills(models.Model):
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Empresa'
    )
    activity_code = models.ForeignKey(
        'Activity',
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        verbose_name='Atividade'
    )
    # skills_code = models.ForeignKey(
    #     'workforces.Skills',
    #     models.DO_NOTHING,
    #     db_column='CODHABILIDADE',
    #     verbose_name='Código da Habilidade'
    # )
    #codhabilidade = models.ForeignKey('FHabilidade', models.DO_NOTHING, db_column='CODHABILIDADE')  # Field name made lowercase.
    amount_skills = models.IntegerField(
        db_column='QTDHABILIDADE',
        blank=True,
        null=True,
        verbose_name='Quantidade de Habilidade'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Filial'
    )
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )

    class Meta:
        managed = False
        db_table = 'F_ATIVHABILIDADES'
        #unique_together = (('codcoligada', 'codatividade', 'codhabilidade'),)
        verbose_name = 'Habilidade da Atividade'
        verbose_name_plural = 'Habilidades da Atividade'

    def __str__(self):
        return f"Habilidade self.skills_code para Atividade {self.activity_code_id} (Empresa: {self.company_code_id})"