from django.db import models


class ProductionCalendar(models.Model):
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
    description = models.CharField( # Changed from 'dsccalendario'
        db_column='DSCCALENDARIO',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Descrição do Calendário'
    )  # Field name made lowercase.
    year = models.CharField( # Changed from 'anocalendario'
        db_column='ANOCALENDARIO',
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Ano do Calendário'
    )  # Field name made lowercase.
    start_date = models.DateTimeField( # Changed from 'datainicio'
        db_column='DATAINICIO',
        blank=True,
        null=True,
        verbose_name='Data de Início'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_CALENDARIOPRODUCAO'
        verbose_name = 'Calendário de Produção'
        verbose_name_plural = 'Calendários de Produção'

    def __str__(self):
        return self.description if self.description else f"Calendário {self.code} ({self.year})"


class ShiftNonWorkingDay(models.Model):
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )  # Field name made lowercase.
    production_calendar = models.ForeignKey(
        'ProductionCalendar',  # Assuming FCalendarioproducao translates to ProductionCalendar
        models.DO_NOTHING,
        db_column='CODCALENDARIO',
        blank=True,
        null=True,
        verbose_name='Calendário de Produção'
    )  # Field name made lowercase.
    non_working_day = models.DateTimeField(
        db_column='DIASNAOUTEIS',
        blank=True,
        null=True,
        verbose_name='Dia Não Útil'
    )  # Field name made lowercase.
    start_time = models.CharField(
        db_column='HORAINICIO',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Hora de Início'
    )  # Field name made lowercase.
    end_time = models.CharField(
        db_column='HORAFIM',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Hora de Fim'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_TURNOSDIASNAOUTEIS'
        verbose_name = 'Turno em Dia Não Útil'
        verbose_name_plural = 'Turnos em Dias Não Úteis'

    def __str__(self):
        return self.description if self.description else f"Turno em Dia Não Útil ({self.non_working_day})"
