# Generated by Django 2.0.7 on 2018-07-07 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NebAddress',
            fields=[
                ('address', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=0, max_digits=50)),
                ('nonce', models.PositiveIntegerField()),
                ('address_type', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NebBlock',
            fields=[
                ('hash', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('height', models.PositiveIntegerField(unique=True)),
                ('nonce', models.PositiveIntegerField()),
                ('timestamp', models.IntegerField()),
                ('miner', models.CharField(db_index=True, max_length=64)),
                ('coinbase', models.CharField(db_index=True, max_length=48)),
                ('is_finality', models.BooleanField(default=False)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='nebscan.NebBlock')),
            ],
        ),
        migrations.CreateModel(
            name='NebTransaction',
            fields=[
                ('hash', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=0, max_digits=50)),
                ('nonce', models.PositiveIntegerField()),
                ('timestamp', models.IntegerField()),
                ('transaction_type', models.CharField(db_index=True, max_length=64)),
                ('data', models.TextField(null=True)),
                ('gas_price', models.PositiveIntegerField()),
                ('gas_limit', models.PositiveIntegerField()),
                ('gas_used', models.PositiveIntegerField()),
                ('status', models.SmallIntegerField()),
                ('execute_error', models.TextField(default='')),
                ('execute_result', models.TextField(default='')),
                ('block_hash', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nebscan.NebBlock')),
                ('contract_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract_address_set', to='nebscan.NebAddress')),
                ('from_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='out_transaction_set', to='nebscan.NebAddress')),
                ('to_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='in_transaction_set', to='nebscan.NebAddress')),
            ],
        ),
    ]