from django.db import models


class Workstation(models.Model):
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
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    production_calendar = models.ForeignKey(
        'calendar_production.ProductionCalendar',  # Assuming 'FCalendarioproducao' translates to 'ProductionCalendar'
        models.DO_NOTHING,
        db_column='CODCALENDARIO',
        blank=True,
        null=True,
        verbose_name='Calendário de Produção',
        related_name='workstations_main_calendar' # Added distinct related_name
    )  # Field name made lowercase.
    description = models.CharField( # Changed from 'descposto'
        db_column='DESCPOSTO',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Descrição do Posto'
    )  # Field name made lowercase.
    calendar1 = models.ForeignKey( # Changed from 'codcalend1'
        'calendar_production.ProductionCalendar',  # Assuming 'FCalendarioproducao' translates to 'ProductionCalendar'
        models.DO_NOTHING,
        db_column='CODCALEND1',
        related_name='workstations_calendar1', # Changed from default 'fpostos_codcalend1_set'
        blank=True,
        null=True,
        verbose_name='Calendário 1'
    )  # Field name made lowercase.
    calendar2 = models.ForeignKey( # Changed from 'codcalend2'
        'calendar_production.ProductionCalendar',  # Assuming 'FCalendarioproducao' translates to 'ProductionCalendar'
        models.DO_NOTHING,
        db_column='CODCALEND2',
        related_name='workstations_calendar2', # Changed from default 'fpostos_codcalend2_set'
        blank=True,
        null=True,
        verbose_name='Calendário 2'
    )  # Field name made lowercase.
    cost_center_code = models.CharField(
        db_column='CODCCUSTO',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Código do Centro de Custo'
    )  # Field name made lowercase.
    hourly_cost = models.DecimalField( # Changed from 'custohoraposto'
        db_column='CUSTOHORAPOSTO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Hora do Posto'
    )  # Field name made lowercase.
    is_external = models.IntegerField( # Changed from 'postoexterno'
        db_column='POSTOEXTERNO',
        blank=True,
        null=True,
        verbose_name='Posto Externo'
    )  # Field name made lowercase.
    is_active = models.IntegerField( # Changed from 'ativo'
        db_column='ATIVO',
        blank=True,
        null=True,
        verbose_name='Ativo'
    )  # Field name made lowercase.
    effectiveness = models.DecimalField(
        db_column='EFETIVIDADE',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Efetividade'
    )  # Field name made lowercase.
    monthly_cost = models.DecimalField( # Changed from 'customes'
        db_column='CUSTOMES',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Mensal'
    )  # Field name made lowercase.
    stock_location_code = models.IntegerField(
        db_column='CODLOCALESTOQUE',
        blank=True,
        null=True,
        verbose_name='Código do Local de Estoque'
    )  # Field name made lowercase.
    cost_sql = models.TextField(
        db_column='SQL_CUSTO',
        blank=True,
        null=True,
        verbose_name='SQL de Custo'
    )  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'F_POSTOS'
        verbose_name = 'Posto de Trabalho'
        verbose_name_plural = 'Postos de Trabalho'

    def __str__(self):
        return self.description if self.description else f"Posto de Trabalho {self.code}"