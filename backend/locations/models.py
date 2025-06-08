from django.db import models


class Municipality(models.Model):
    code = models.AutoField(db_column='CODIGO', primary_key=True, verbose_name="Código")
    identifier = models.CharField(db_column='IDENTIFICADOR', max_length=30, blank=True, null=True, verbose_name="Identificador")
    name = models.CharField(db_column='NOME', max_length=255, blank=True, null=True, verbose_name="Nome da Cidade")  # Field name made lowercase.
    code_state = models.ForeignKey('State', models.DO_NOTHING, db_column='CODIGO_UF', blank=True, null=True, verbose_name="Código do Estado")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'G_MUNICIPIOS'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

class State(models.Model):
    code = models.AutoField(db_column='CODIGO', primary_key=True, verbose_name='Código')
    identifier = models.CharField(db_column='IDENTIFICADOR', max_length=30, verbose_name='Identificador')
    name = models.CharField(db_column='NOME', max_length=255, verbose_name="Nome do Estado")
    code_country = models.ForeignKey('Country', models.DO_NOTHING, db_column='CODIGO_PAIS', verbose_name="Código do País")
    st_state_registration = models.CharField(db_column='INSCRICAOESTADUAL_ST', max_length=20, blank=True, null=True, verbose_name="Inscrição Estadual ST")
    uses_calculation_inside = models.IntegerField(db_column='UTILIZA_CALCULO_POR_DENTRO', blank=True, null=True, verbose_name="Utiliza Cálculo por Dentro")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'G_UF'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Country(models.Model):
    code = models.AutoField(db_column='CODIGO', primary_key=True, verbose_name="Código")
    identifier = models.CharField(db_column='IDENTIFICADOR', max_length=30, verbose_name="Identificador")
    name = models.CharField(db_column='NOME', max_length=255, verbose_name="Nome do País")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'G_PAIS'
        verbose_name = 'País'
        verbose_name_plural = 'Países'