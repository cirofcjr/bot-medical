# Generated by Django 2.1.2 on 2018-10-18 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20181018_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialidade',
            name='descricao',
            field=models.TextField(null=True, verbose_name='Descrição'),
        ),
    ]