# Generated by Django 5.0.3 on 2024-05-25 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='comp_sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.competitionssports', verbose_name='comp_sport'),
        ),
    ]
