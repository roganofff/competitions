# Generated by Django 5.0.3 on 2024-04-30 06:08

import competitions_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions_app', '0002_remove_stage_competition_id_competition_sports_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='stage_date',
            field=models.DateField(default=competitions_app.models.get_datetime, verbose_name='stage_date'),
        ),
    ]