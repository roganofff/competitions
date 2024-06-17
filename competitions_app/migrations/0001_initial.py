# Generated by Django 5.0.3 on 2024-05-25 18:00

import competitions_app.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('competition_start', models.DateField(blank=True, default=competitions_app.models._get_datetime, null=True, verbose_name='competition_start')),
                ('competition_end', models.DateField(blank=True, default=competitions_app.models._get_datetime, null=True, verbose_name='competition_end')),
            ],
            options={
                'verbose_name': 'Competition',
                'verbose_name_plural': 'Competitions',
                'db_table': '"crud_api"."competition"',
                'ordering': ['competition_start', 'competition_end', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=11, validators=[competitions_app.models._check_positive], verbose_name='money')),
                ('token', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': '"crud_api"."client"',
            },
        ),
        migrations.CreateModel(
            name='CompetitionsSports',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('competition_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitions_app.competition', verbose_name='competition_id')),
            ],
            options={
                'verbose_name': 'relationship competition sports',
                'verbose_name_plural': 'relationships competition sports',
                'db_table': '"crud_api"."competitions_sports"',
                'ordering': ['competition_id', 'sport_id'],
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='description')),
                ('competitions', models.ManyToManyField(through='competitions_app.CompetitionsSports', to='competitions_app.competition', verbose_name='competitions')),
            ],
            options={
                'verbose_name': 'Sport',
                'verbose_name_plural': 'Sports',
                'db_table': '"crud_api"."sport"',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='competitionssports',
            name='sport_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.sport', verbose_name='sport_id'),
        ),
        migrations.AddField(
            model_name='competition',
            name='sports',
            field=models.ManyToManyField(through='competitions_app.CompetitionsSports', to='competitions_app.sport', verbose_name='sports'),
        ),
        migrations.CreateModel(
            name='SportClient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('cleint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.client', verbose_name='client')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.sport', verbose_name='sport')),
            ],
            options={
                'verbose_name': 'relationship sport client',
                'verbose_name_plural': 'relationships sport client',
                'db_table': '"crud_api"."sport_client"',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='sports',
            field=models.ManyToManyField(through='competitions_app.SportClient', to='competitions_app.sport', verbose_name='sports'),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('created', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=competitions_app.models._get_datetime, null=True, validators=[competitions_app.models._check_modified], verbose_name='modified')),
                ('stage_date', models.DateField(default=competitions_app.models._get_datetime, verbose_name='stage_date')),
                ('place', models.TextField(blank=True, max_length=150, null=True, verbose_name='place')),
                ('comp_sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.competitionssports', verbose_name='comp_sport')),
            ],
            options={
                'verbose_name': 'Stage',
                'verbose_name_plural': 'Stages',
                'db_table': '"crud_api"."stage"',
                'ordering': ['stage_date', 'name'],
            },
        ),
        migrations.AddConstraint(
            model_name='competition',
            constraint=models.CheckConstraint(check=models.Q(('competition_end__gt', models.F('competition_start'))), name='check_start_date', violation_error_message="Competition cannot end before it's start."),
        ),
    ]
