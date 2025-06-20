# Generated by Django 5.0.14 on 2025-06-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('code', models.AutoField(db_column='CODIGO', primary_key=True, serialize=False, verbose_name='Código')),
                ('description', models.CharField(blank=True, db_column='DESCRICAO', max_length=200, null=True, verbose_name='Descrição')),
                ('type', models.IntegerField(blank=True, db_column='TIPO', null=True, verbose_name='Tipo')),
                ('structure_id', models.CharField(blank=True, db_column='IDESTRUTURA', max_length=20, null=True, verbose_name='ID da Estrutura')),
                ('indirect_cost', models.DecimalField(blank=True, db_column='CUSTOINDIRETO', decimal_places=3, max_digits=10, null=True, verbose_name='Custo Indireto')),
                ('planned_structure_cost', models.DecimalField(blank=True, db_column='CUSTOPREVISTOESTRUTURA', decimal_places=3, max_digits=10, null=True, verbose_name='Custo Previsto da Estrutura')),
                ('sequence', models.IntegerField(blank=True, db_column='SEQUENCIA', null=True, verbose_name='Sequência')),
                ('image_address', models.CharField(blank=True, db_column='ENDERECOIMAGEM', max_length=250, null=True, verbose_name='Endereço da Imagem')),
                ('tech_data_multiple_quantity', models.DecimalField(blank=True, db_column='DADOS_TEC_MULTIPLO_QTDE', decimal_places=8, max_digits=18, null=True, verbose_name='Dados Téc. Múltiplo Quantidade')),
                ('tech_data_multiple_standard_width', models.DecimalField(blank=True, db_column='DADOS_TEC_MULTIPLO_PADRAO_LARGURA', decimal_places=8, max_digits=18, null=True, verbose_name='Dados Téc. Múltiplo Padrão Largura')),
                ('tech_data_multiple_standard_length', models.DecimalField(blank=True, db_column='DADOS_TEC_MULTIPLO_PADRAO_COMPRIMENTO', decimal_places=8, max_digits=18, null=True, verbose_name='Dados Téc. Múltiplo Padrão Comprimento')),
                ('gear_validation', models.IntegerField(blank=True, db_column='VALIDACAO_ENGRENAGEM', null=True, verbose_name='Validação Engrenagem')),
                ('wing_or_handle', models.IntegerField(blank=True, db_column='ASA', null=True, verbose_name='Asa/Alça')),
                ('z_factor', models.IntegerField(blank=True, db_column='Z', null=True, verbose_name='Fator Z')),
                ('revision1_flag', models.CharField(blank=True, db_column='REVISAO1', max_length=1, null=True, verbose_name='Revisão 1 (Flag)')),
                ('revision_number', models.IntegerField(blank=True, db_column='REVISAO', null=True, verbose_name='Revisão (Número)')),
                ('is_main', models.IntegerField(blank=True, db_column='PRINCIPAL', null=True, verbose_name='Principal')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_column='DATA_CRIACAO', null=True, verbose_name='Data de Criação')),
                ('loss_percentage', models.DecimalField(blank=True, db_column='PERCENTUAL_PERDA', decimal_places=10, max_digits=20, null=True, verbose_name='Percentual de Perda')),
                ('is_active_flag1', models.IntegerField(blank=True, db_column='ATIVA', null=True, verbose_name='Ativa (Flag 1)')),
                ('is_active_flag2', models.IntegerField(blank=True, db_column='ATIVO', null=True, verbose_name='Ativo (Flag 2)')),
                ('observation', models.TextField(blank=True, db_column='OBSERVACAO', null=True, verbose_name='Observação')),
                ('mrp_orders_balance', models.DecimalField(blank=True, db_column='SALDO_ORDENS_MRP', decimal_places=10, max_digits=20, null=True, verbose_name='Saldo Ordens MRP')),
            ],
            options={
                'verbose_name': 'Estrutura',
                'verbose_name_plural': 'Estruturas',
                'db_table': 'F_ESTRUTURA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureActivity',
            fields=[
                ('process_time', models.DecimalField(blank=True, db_column='TEMPOPROCESSO', decimal_places=10, max_digits=20, null=True, verbose_name='Tempo de Processo')),
                ('process_type', models.IntegerField(blank=True, db_column='TIPOPROCESSO', null=True, verbose_name='Tipo de Processo')),
                ('sequence', models.IntegerField(blank=True, db_column='SEQUENCIA', null=True, verbose_name='Sequência')),
                ('code', models.AutoField(db_column='CODIGO', primary_key=True, serialize=False, verbose_name='Código')),
                ('cycle_time', models.DecimalField(blank=True, db_column='TEMPOCICLO', decimal_places=10, max_digits=20, null=True, verbose_name='Tempo de Ciclo')),
                ('cnc_program', models.CharField(blank=True, db_column='PROGRAMACNC', max_length=100, null=True, verbose_name='Programa CNC')),
                ('preparation_notes', models.TextField(blank=True, db_column='PREPARACAO', null=True, verbose_name='Preparação (Notas)')),
                ('execution_notes', models.TextField(blank=True, db_column='EXECUCAO', null=True, verbose_name='Execução (Notas)')),
                ('verification_notes', models.TextField(blank=True, db_column='CONFERENCIA', null=True, verbose_name='Conferência (Notas)')),
            ],
            options={
                'verbose_name': 'Atividade da Estrutura',
                'verbose_name_plural': 'Atividades da Estrutura',
                'db_table': 'F_ATVESTRUTURA',
                'managed': False,
            },
        ),
    ]
