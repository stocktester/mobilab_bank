# Generated by Django 4.0.3 on 2022-04-01 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='modified',
        ),
    ]
