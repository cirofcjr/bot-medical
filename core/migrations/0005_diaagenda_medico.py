# Generated by Django 2.1.2 on 2018-10-15 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20181015_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaagenda',
            name='medico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Medico'),
            preserve_default=False,
        ),
    ]
