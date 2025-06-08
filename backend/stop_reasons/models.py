from django.db import models


class StopReason(models.Model):
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
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    stoppage_id = models.CharField( # Changed from idparada
        db_column='IDPARADA',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID da Parada'
    )  # Field name made lowercase.
    description = models.CharField( # Changed from descricaoparada
        db_column='DESCRICAOPARADA',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição da Parada'
    )  # Field name made lowercase.
    is_active = models.IntegerField( # Changed from ativo
        db_column='ATIVO',
        blank=True,
        null=True,
        verbose_name='Ativo'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_RAZOESPARADA'
        verbose_name = 'Razão da Parada'
        verbose_name_plural = 'Razões da Parada'

    def __str__(self):
        return self.description if self.description else f"Razão {self.stoppage_id or self.code}"