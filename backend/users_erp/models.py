from django.db import models


class Employee(models.Model):
    code = models.AutoField(
        db_column='CODIGO',
        primary_key=True,
        verbose_name='Código'
    )  # Field name made lowercase.
    name = models.CharField(
        db_column='NOME',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Nome'
    )  # Field name made lowercase.
    email = models.CharField(
        db_column='EMAIL',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='E-mail'
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
    phone = models.CharField(
        db_column='TELEFONE',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )  # Field name made lowercase.
    address = models.CharField(
        db_column='ENDERECO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Endereço'
    )  # Field name made lowercase.
    city_code_fk = models.IntegerField( # Suffix for clarity as it's an integer code
        db_column='CODCIDADE',
        blank=True,
        null=True,
        verbose_name='Código da Cidade (Ref)'
    )  # Field name made lowercase.
    user_profile_code = models.IntegerField(
        db_column='CODPERFILUSUARIO',
        blank=True,
        null=True,
        verbose_name='Código do Perfil de Usuário'
    )  # Field name made lowercase.
    username = models.CharField( # Changed from 'usuario'
        db_column='USUARIO',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Usuário (Login)'
    )  # Field name made lowercase.
    password = models.CharField( # Changed from 'senha'
        db_column='SENHA',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Senha'
    )  # Field name made lowercase.
    sector_code = models.IntegerField(
        db_column='CODSETOR',
        blank=True,
        null=True,
        verbose_name='Código do Setor'
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
    uc_login = models.CharField( # 'uc' prefix kept if it's a system identifier
        db_column='UCLOGIN',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='UC Login'
    )  # Field name made lowercase.
    uc_password = models.CharField(
        db_column='UCPASSWORD',
        max_length=250,
        blank=True,
        null=True,
        verbose_name='UC Senha'
    )  # Field name made lowercase.
    uc_password_expired_flag = models.CharField( # More descriptive
        db_column='UCPASSEXPIRED',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='UC Senha Expirada (Flag)'
    )  # Field name made lowercase.
    uc_user_expired_flag = models.IntegerField( # More descriptive
        db_column='UCUSEREXPIRED',
        blank=True,
        null=True,
        verbose_name='UC Usuário Expirado (Flag)'
    )  # Field name made lowercase.
    uc_user_days_sun = models.IntegerField( # Kept as is, meaning might be specific
        db_column='UCUSERDAYSSUN',
        blank=True,
        null=True,
        verbose_name='UC Dias Usuário Sol' # Or a more specific known meaning
    )  # Field name made lowercase.
    uc_is_privileged = models.IntegerField( # More descriptive
        db_column='UCPRIVILEGED',
        blank=True,
        null=True,
        verbose_name='UC Privilegiado'
    )  # Field name made lowercase.
    uc_type_rec = models.CharField( # Kept as is
        db_column='UCTYPEREC',
        max_length=1,
        blank=True,
        null=True,
        verbose_name='UC Tipo Rec.'
    )  # Field name made lowercase.
    uc_profile_code = models.IntegerField( # More descriptive
        db_column='UCPROFILE',
        blank=True,
        null=True,
        verbose_name='UC Código do Perfil'
    )  # Field name made lowercase.
    uc_key = models.CharField(
        db_column='UCKEY',
        max_length=250,
        blank=True,
        null=True,
        verbose_name='UC Chave'
    )  # Field name made lowercase.
    uc_email = models.CharField(
        db_column='UCEMAIL',
        max_length=150,
        blank=True,
        null=True,
        verbose_name='UC E-mail'
    )  # Field name made lowercase.
    uc_user_id = models.IntegerField(
        db_column='UCIDUSER',
        blank=True,
        null=True,
        verbose_name='UC ID Usuário'
    )  # Field name made lowercase.
    uc_username = models.CharField(
        db_column='UCUSERNAME',
        max_length=30,
        blank=True,
        null=True,
        verbose_name='UC Nome de Usuário'
    )  # Field name made lowercase.
    municipality = models.ForeignKey( # Assuming 'GMunicipios' will be 'Municipality'
        'locations.Municipality',
        models.DO_NOTHING,
        db_column='CODIGO_MUNICIPIOS',
        blank=True,
        null=True,
        verbose_name='Município'
    )  # Field name made lowercase.
    customer_supplier_fk = models.IntegerField(
        db_column='CODIGO_CLIFORN',
        blank=True,
        null=True,
        verbose_name='Cliente/Fornecedor'
    )  # Field name made lowercase.
    uc_is_inactive = models.IntegerField( # More descriptive
        db_column='UCINATIVE',
        blank=True,
        null=True,
        verbose_name='UC Inativo'
    )  # Field name made lowercase.
    allows_release_movements = models.IntegerField(
        db_column='PERMITE_LIBERAR_MOVIMENTOS',
        blank=True,
        null=True,
        verbose_name='Permite Liberar Movimentos'
    )  # Field name made lowercase.
    sat_dll_path = models.CharField( # SAT = Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos
        db_column='CAMINHO_DLL_SAT',
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Caminho DLL SAT'
    )  # Field name made lowercase.
    sat_cashier_number = models.CharField(
        db_column='NUMERO_CAIXA_SAT',
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Número Caixa SAT'
    )  # Field name made lowercase.
    email_smtp_server = models.CharField(
        db_column='EMAIL_SERVIDOR_SMTP',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='E-mail Servidor SMTP'
    )  # Field name made lowercase.
    email_smtp_port = models.CharField(
        db_column='EMAIL_PORTA_SMTP',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='E-mail Porta SMTP'
    )  # Field name made lowercase.
    email_user = models.CharField(
        db_column='EMAIL_USUARIO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='E-mail Usuário'
    )  # Field name made lowercase.
    email_password = models.CharField(
        db_column='EMAIL_SENHA',
        max_length=50,
        blank=True,
        null=True,
        verbose_name='E-mail Senha'
    )  # Field name made lowercase.
    email_default_subject = models.CharField(
        db_column='EMAIL_ASSUNTO_PADRAO',
        max_length=100,
        blank=True,
        null=True,
        verbose_name='E-mail Assunto Padrão'
    )  # Field name made lowercase.
    email_default_message = models.CharField(
        db_column='EMAIL_MENSAGEM_PADRAO',
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='E-mail Mensagem Padrão'
    )  # Field name made lowercase.
    email_uses_authentication = models.IntegerField(
        db_column='EMAIL_UTILIZA_AUTENTICACAO',
        blank=True,
        null=True,
        verbose_name='E-mail Utiliza Autenticação'
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COLABORADOR'
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

    def __str__(self):
        return self.name if self.name else f"Colaborador {self.code}"

