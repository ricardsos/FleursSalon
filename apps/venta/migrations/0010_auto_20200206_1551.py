# Generated by Django 3.0.2 on 2020-02-06 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0009_auto_20200126_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='codigo',
            field=models.CharField(max_length=100, verbose_name='Código'),
        ),
    ]
