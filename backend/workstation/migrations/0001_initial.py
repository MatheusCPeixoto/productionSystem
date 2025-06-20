# Generated by Django 5.0.14 on 2025-06-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workstation',
            fields=[
                ('code', models.AutoField(db_column='CODIGO', primary_key=True, serialize=False, verbose_name='Código')),
                ('description', models.CharField(blank=True, db_column='DESCPOSTO', max_length=60, null=True, verbose_name='Descrição do Posto')),
                ('cost_center_code', models.CharField(blank=True, db_column='CODCCUSTO', max_length=30, null=True, verbose_name='Código do Centro de Custo')),
                ('hourly_cost', models.DecimalField(blank=True, db_column='CUSTOHORAPOSTO', decimal_places=3, max_digits=10, null=True, verbose_name='Custo Hora do Posto')),
                ('is_external', models.IntegerField(blank=True, db_column='POSTOEXTERNO', null=True, verbose_name='Posto Externo')),
                ('is_active', models.IntegerField(blank=True, db_column='ATIVO', null=True, verbose_name='Ativo')),
                ('effectiveness', models.DecimalField(blank=True, db_column='EFETIVIDADE', decimal_places=3, max_digits=6, null=True, verbose_name='Efetividade')),
                ('monthly_cost', models.DecimalField(blank=True, db_column='CUSTOMES', decimal_places=3, max_digits=10, null=True, verbose_name='Custo Mensal')),
                ('stock_location_code', models.IntegerField(blank=True, db_column='CODLOCALESTOQUE', null=True, verbose_name='Código do Local de Estoque')),
                ('cost_sql', models.TextField(blank=True, db_column='SQL_CUSTO', null=True, verbose_name='SQL de Custo')),
            ],
            options={
                'verbose_name': 'Posto de Trabalho',
                'verbose_name_plural': 'Postos de Trabalho',
                'db_table': 'F_POSTOS',
                'managed': False,
            },
        ),
    ]
