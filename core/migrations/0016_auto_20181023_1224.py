# Generated by Django 2.1.2 on 2018-10-23 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20181018_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diaagenda',
            name='turnos',
        ),
        migrations.AddField(
            model_name='diaagenda',
            name='turnos',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Turno'),
            preserve_default=False,
        ),
    ]
