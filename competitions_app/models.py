from datetime import date, datetime, timezone
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


MAX_LENGTH_NAME = 100
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_PLACE = 150


def get_datetime():
    return datetime.now(timezone.utc)


def _check_created(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )


def _check_modified(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.TextField(_('name'), null=False, blank=False, max_length=MAX_LENGTH_NAME)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[_check_created],
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[_check_modified]
    )

    class Meta:
        abstract = True


class Competition(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    competition_start = models.DateField(
        _('competition_start'),
        null=True, blank=True,
        default=get_datetime,
    )
    competition_end = models.DateField(
        _('competition_end'),
        null=True, blank=True,
        default=get_datetime,
    )

    sports = models.ManyToManyField('Sport', verbose_name=_('sports'), through='CompetitionsSports')

    def __str__(self) -> str:
        return f'{self.name}: {self.competition_start}—{self.competition_end}.'

    class Meta:
        db_table = '"crud_api"."competition"'
        ordering = ['name', 'competition_start', 'competition_end']
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')
        constraints = [
            CheckConstraint(
                check = Q(competition_end__gt=F('competition_start')), 
                name = 'check_start_date',
                violation_error_message = _("Competition cannot end before it's start."),
            ),
        ]


class Sport(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    description = models.TextField(
        _('description'),
        null=True, blank=True,
        max_length=MAX_LENGTH_DESCRIPTION
    )

    competitions = models.ManyToManyField(Competition, verbose_name=_('competitions'), through='CompetitionsSports')

    def __str__(self) -> str:
        return f'{self.name}. {self.description}'

    class Meta:
        db_table = '"crud_api"."sport"'
        ordering = ['name']
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')


class Stage(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    stage_date = models.DateField(_('stage_date'), null=False, blank=False, default=get_datetime)
    place = models.TextField(_('place'), null=True, blank=True, max_length=MAX_LENGTH_PLACE)
    
    sport_id = models.ForeignKey(Sport, verbose_name=_('sport_id'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}: {self.place}({self.stage_date}).'

    class Meta:
        db_table = '"crud_api"."stage"'
        ordering = ['name', 'stage_date']
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')
        constraints = [
            CheckConstraint(
                check = Q(stage_date__gt=F('"Competition"."competition_start"')), 
                name = 'check_stage_date',
                violation_error_message = _("Competition's stage cannot be held before the competition."),
            ),
        ]


class CompetitionsSports(CreatedMixin, ModifiedMixin):
    competition_id = models.ForeignKey(
        Competition,
        verbose_name=_('competition_id'),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    sport_id = models.ForeignKey(
        Sport,
        verbose_name=_('sport_id'),
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = '"crud_api"."competitions_sports"'
        ordering = ['competition_id', 'sport_id']
        verbose_name = _('relationship competition sports')
        verbose_name_plural = _('relationships competition sports')