# Generated by Django 2.1.2 on 2018-10-15 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181015_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaAgenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EscalaTempo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.TimeField()),
                ('fim', models.TimeField()),
                ('dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tempo', to='core.DiaAgenda')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.TimeField()),
                ('fim', models.TimeField()),
            ],
        ),
        migrations.AddField(
            model_name='diaagenda',
            name='turnos',
            field=models.ManyToManyField(to='core.Turno'),
        ),
    ]