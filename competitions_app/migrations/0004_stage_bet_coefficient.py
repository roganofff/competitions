# Generated by Django 5.0.3 on 2024-06-16 16:30

import competitions_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions_app', '0003_alter_stage_comp_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='bet_coefficient',
            field=models.DecimalField(decimal_places=2, default=competitions_app.models._get_random_bet_coefficient, max_digits=5, verbose_name='bet_coefficient'),
        ),
    ]
