# Generated by Django 4.0.3 on 2022-03-31 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_alter_bankaccount_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='balance',
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='bank.bankcustomer'),
        ),
    ]
