from datetime import datetime, timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


MAX_LENGTH_NAME = 100
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_PLACE = 150


def get_datetime():
    return datetime.now(timezone.utc)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.TextField(_('competition_name'), null=False, blank=False, max_length=MAX_LENGTH_NAME)

    class Meta:
        abstract = True


class Competition(UUIDMixin, NameMixin):
    competition_start = models.DateField(_('competition_start'), null=True, blank=True, default=get_datetime)
    competition_end = models.DateField(_('competition_end'), null=True, blank=True, default=get_datetime)

    class Meta:
        db_table = '"crud_api"."competition"'
        ordering = ['name', 'competition_start', 'competition_end']
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')


class Sport(UUIDMixin, NameMixin):
    description = models.TextField(_('description'), null=True, blank=True, max_length=MAX_LENGTH_DESCRIPTION)

    class Meta:
        db_table = '"crud_api"."sport"'
        ordering = ['name']
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')


class Stage(UUIDMixin, NameMixin):
    stage_date = models.DateField(_('stage_date'), null=True, blank=True, default=get_datetime)
    place = models.TextField(_('place'), null=True, blank=True, max_length=MAX_LENGTH_PLACE)
    
    competition_id = models.ForeignKey(Competition, verbose_name=_('competition_id'), on_delete=models.CASCADE)
    sport_id = models.ForeignKey(Sport, verbose_name=_('sport_id'), on_delete=models.CASCADE)

    class Meta:
        db_table = '"crud_api"."stage"'
        ordering = ['name', 'stage_date']
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')


class CompetitionsSports(models.Model):
    competition_id = models.ForeignKey(Competition, verbose_name=_('competition_id'), on_delete=models.CASCADE)
    sport_id = models.ForeignKey(Sport, verbose_name=_('sport_id'), on_delete=models.CASCADE)

    class Meta:
        db_table = '"crud_api"."competitions_sports"'
        ordering = ['competition_id', 'sport_id']
        verbose_name = _('relationship competition sports')
        verbose_name_plural = _('relationships competition sports')