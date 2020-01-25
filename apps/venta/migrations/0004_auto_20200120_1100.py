# Generated by Django 3.0.2 on 2020-01-20 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
        ('venta', '0003_auto_20200120_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineadeproducto',
            name='colaborador',
        ),
        migrations.AddField(
            model_name='lineadeservicio',
            name='colaborador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usuario.Colaborador'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lineadeservicio',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Precio'),
        ),
    ]
