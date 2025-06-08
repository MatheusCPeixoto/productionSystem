from django.db import models


class Workforce(models.Model):
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
        verbose_name='Código da Coligada (Ref)'
    )  # Field name made lowercase.
    name = models.CharField(
        db_column='NOME',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Nome'
    )  # Field name made lowercase.
    street = models.CharField(
        db_column='RUA',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Rua'
    )  # Field name made lowercase.
    street_number = models.CharField(
        db_column='NUMERO',
        max_length=8,
        blank=True,
        null=True,
        verbose_name='Número'
    )  # Field name made lowercase.
    neighborhood = models.CharField(
        db_column='BAIRRO',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Bairro'
    )  # Field name made lowercase.
    birth_date = models.DateTimeField(
        db_column='DATANASCIMENTO',
        blank=True,
        null=True,
        verbose_name='Data de Nascimento'
    )  # Field name made lowercase.
    rg = models.CharField(
        db_column='RG',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='RG'
    )  # Field name made lowercase.
    cpf = models.CharField(
        db_column='CPF',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CPF'
    )  # Field name made lowercase.
    phone1 = models.CharField( # Changed from 'fone'
        db_column='FONE',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone 1'
    )  # Field name made lowercase.
    father_name = models.CharField(
        db_column='NOMEPAI',
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Nome do Pai'
    )  # Field name made lowercase.
    mother_name = models.CharField(
        db_column='NOMEMAE',
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Nome da Mãe'
    )  # Field name made lowercase.
    city_name = models.CharField( # Changed from 'cidade' as there's 'codcidade'
        db_column='CIDADE',
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Nome da Cidade'
    )  # Field name made lowercase.
    state_uf = models.CharField( # Changed from 'uf' for clarity
        db_column='UF',
        max_length=2,
        blank=True,
        null=True,
        verbose_name='UF'
    )  # Field name made lowercase.
    zip_code = models.CharField( # Changed from 'cep'
        db_column='CEP',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='CEP'
    )  # Field name made lowercase.
    phone2 = models.CharField( # Changed from 'telefone'
        db_column='TELEFONE',
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone 2'
    )  # Field name made lowercase.
    is_active = models.IntegerField( # Changed from 'ativa'
        db_column='ATIVA',
        blank=True,
        null=True,
        verbose_name='Ativo'
    )  # Field name made lowercase.
    hourly_cost = models.DecimalField(
        db_column='CUSTOHORAMO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Hora M.O.'
    )  # Field name made lowercase.
    monthly_cost = models.DecimalField(
        db_column='CUSTOMESMO',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Custo Mês M.O.'
    )  # Field name made lowercase.
    effectiveness = models.DecimalField(
        db_column='EFETIVIDADE',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='Efetividade'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial'
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
    employee_id_plate = models.CharField( # 'Chapa' can mean employee ID plate
        db_column='CHAPA',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Chapa (ID Funcionário)'
    )  # Field name made lowercase.
    badge_number = models.CharField( # 'Cracha' means badge
        db_column='CRACHA',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Crachá'
    )  # Field name made lowercase.
    work_shift_minutes = models.IntegerField(
        db_column='TT_TURNO_TRAB_MINUTOS',
        blank=True,
        null=True,
        verbose_name='Total Turno de Trabalho (Minutos)'
    )  # Field name made lowercase.
    workforce_id_text = models.CharField( # Changed from 'idmaoobra'
        db_column='IDMAOOBRA',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ID Mão de Obra (Texto)'
    )  # Field name made lowercase.
    city_code = models.ForeignKey(
        'locations.Municipality',
        models.DO_NOTHING,
        db_column='codcidade', # Keeping db_column as is
        blank=True,
        null=True,
        verbose_name='Código da Cidade (Ref)'
    )
    cost_sql = models.TextField(
        db_column='SQL_CUSTO',
        blank=True,
        null=True,
        verbose_name='SQL de Custo'
    )  # Field name made lowercase. This field type is a guess.
    cf_sector = models.CharField( # Custom field, keeping 'cf' prefix
        db_column='CF_SETOR',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='CF Setor'
    )  # Field name made lowercase.
    cf_situation = models.CharField( # Custom field
        db_column='CF_SITUACAO',
        max_length=300,
        blank=True,
        null=True,
        verbose_name='CF Situação'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_MAOOBRA'
        verbose_name = 'Mão de Obra'
        verbose_name_plural = 'Mão de Obra'

    def __str__(self):
        return self.name if self.name else f"Mão de Obra {self.code}"


class WorkforceCostHistory(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    workforce_code = models.ForeignKey(
        'Workforce',  # Assuming 'FMaoobra' translates to 'Manpower'
        models.DO_NOTHING,
        db_column='CODMAOOBRA',
        blank=True,
        null=True,
        verbose_name='Mão de Obra'
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
        verbose_name='Código da Coligada (Ref)'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )
    is_current = models.IntegerField( # Changed from 'atual'
        db_column='ATUAL',
        blank=True,
        null=True,
        verbose_name='Atual'
    )

    class Meta:
        managed = False
        db_table = 'F_HISTCUSTOMAOOBRA'
        verbose_name = 'Histórico de Custo de Mão de Obra'
        verbose_name_plural = 'Históricos de Custo de Mão de Obra'
        unique_together = (('workforce_code', 'month', 'year', 'company_code', 'branch_code'),) # Suggested unique_together

    def __str__(self):
        return f"Histórico Custo M.O. {self.code} - {self.workforce_code_id} ({self.month}/{self.year})"


class Skill(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )
    description = models.CharField(
        db_column='DESCRICAO',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        blank=True,
        null=True,
        verbose_name='Código da Coligada (Ref)'
    )
    technical_description = models.TextField(
        db_column='DESCRITIVOTECNICO',
        blank=True,
        null=True,
        verbose_name='Descritivo Técnico'
    )
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )
    is_active = models.IntegerField( # Changed from 'ativo'
        db_column='ATIVO',
        blank=True,
        null=True,
        verbose_name='Ativo'
    )

    class Meta:
        managed = False
        db_table = 'F_HABILIDADE'
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.description if self.description else f"Habilidade {self.code}"


class WorkforceSkill(models.Model):
    company_code = models.ForeignKey(
        'enterprises.Company',
        models.DO_NOTHING,
        db_column='CODCOLIGADA',
        verbose_name='Código da Coligada (Ref)'
    )  # Field name made lowercase.
    skill = models.ForeignKey(
        'Skill',  # Assuming FHabilidade translates to Skill
        models.DO_NOTHING,
        db_column='CODHABILIDADE',
        verbose_name='Habilidade'
    )  # Field name made lowercase.
    workforce_code = models.ForeignKey(
        'Workforce',  # Assuming 'FMaoobra' translates to 'Manpower'
        models.DO_NOTHING,
        db_column='CODMAOOBRA',
        verbose_name='Mão de Obra'
    )  # Field name made lowercase.
    branch_code = models.ForeignKey(
        'enterprises.Branch',
        models.DO_NOTHING,
        db_column='CODFILIAL',
        blank=True,
        null=True,
        verbose_name='Código da Filial (Ref)'
    )  # Field name made lowercase.
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'F_MAOOBRAHABILIDADES'
        verbose_name = 'Habilidade da Mão de Obra'
        verbose_name_plural = 'Habilidades da Mão de Obra'

    def __str__(self):
        return f"Habilidade {self.skill_id} para M.O. {self.workforce_code_id} (Coligada: {self.company_code})"