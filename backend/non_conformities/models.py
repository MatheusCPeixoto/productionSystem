from django.db import models

class NonConformance(models.Model):
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
    activity_code = models.ForeignKey(
        'activitys.Activity',  # Assuming 'FAtividade' translates to 'Activity'
        models.DO_NOTHING,
        db_column='CODATIVIDADE',
        blank=True,
        null=True,
        verbose_name='Atividade'
    )  # Field name made lowercase.
    non_conformance_id = models.CharField(
        db_column='IDNAOCONFORMIDADE',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID da Não Conformidade'
    )  # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRICAONCONF',
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descrição da Não Conformidade'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_NAOCONFORMIDADES'
        verbose_name = 'Não Conformidade'
        verbose_name_plural = 'Não Conformidades'

    def __str__(self):
        return self.description if self.description else f"Não Conformidade {self.code}"


class NonConformanceWriteOffItem(models.Model):
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
    )  # Field name made lowercase.
    non_conformance = models.ForeignKey(
        'non_conformities.NonConformance',  # Assuming FNaoconformidades translates to NonConformance
        models.DO_NOTHING,
        db_column='CODNAOCONFORMIDADE',
        verbose_name='Não Conformidade'
    )  # Field name made lowercase.
    product_code = models.ForeignKey(
        'products.Product',  # Assuming 'Gproduto' translates to 'Product'
        models.DO_NOTHING,
        db_column='CODPRODUTO',
        verbose_name='Produto'
    )  # Field name made lowercase.
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_NCONF_ITENSBAIXA'
        verbose_name = 'Item de Baixa de Não Conformidade'
        verbose_name_plural = 'Itens de Baixa de Não Conformidades'

    def __str__(self):
        return f"Item de Baixa {self.code} (NC: {self.non_conformance_id}, Produto: {self.product_code_id})"