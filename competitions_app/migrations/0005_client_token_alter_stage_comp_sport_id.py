# Generated by Django 5.0.3 on 2024-05-15 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions_app', '0004_alter_stage_comp_sport_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]