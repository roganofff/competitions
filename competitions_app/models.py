from datetime import datetime, timezone
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL


MAX_LENGTH_NAME = 100
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_PLACE = 150


def _get_datetime():
    return datetime.now(timezone.utc)


def _check_created(dt: datetime):
    if dt > _get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )


def _check_modified(dt: datetime):
    if dt > _get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )


def _check_positive(number) -> None:
    if number < 0:
        raise ValidationError('value should be equal or greater than zero')


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
        default=_get_datetime,
        validators=[_check_created],
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=_get_datetime,
        validators=[_check_modified]
    )

    class Meta:
        abstract = True


class Competition(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    competition_start = models.DateField(
        _('competition_start'),
        null=True, blank=True,
        default=_get_datetime,
    )
    competition_end = models.DateField(
        _('competition_end'),
        null=True, blank=True,
        default=_get_datetime,
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
    stage_date = models.DateField(_('stage_date'), null=False, blank=False, default=_get_datetime)
    place = models.TextField(_('place'), null=True, blank=True, max_length=MAX_LENGTH_PLACE)
    
    comp_sport = models.ForeignKey(
        'CompetitionsSports',
        verbose_name=_('comp_sport'),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    def __str__(self) -> str:
        return f'{self.name}: {self.place}({self.stage_date}).'

    def clean(self) -> None:
        if self.stage_date < self.comp_sport.competition_id.competition_start:
            raise ValidationError(_('Stage cannot be held before the competition start.'))
        if self.stage_date > self.comp_sport.competition_id.competition_end:
            raise ValidationError(_('Stage cannot be held after the competition end.'))
        return super().clean()

    class Meta:
        db_table = '"crud_api"."stage"'
        ordering = ['name', 'stage_date']
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')


class CompetitionsSports(UUIDMixin, CreatedMixin, ModifiedMixin):
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


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    money = models.DecimalField(
        verbose_name=_('money'),
        decimal_places=2,
        max_digits=11,
        default=0,
        validators=[_check_positive],
    )
    user = models.OneToOneField(AUTH_USER_MODEL, unique=True, verbose_name=_('user'), on_delete=models.CASCADE)
    token = models.CharField(max_length=100, blank=True)
    sports = models.ManyToManyField(Sport, through='SportClient', verbose_name=_('sports'))

    class Meta:
        db_table = '"crud_api"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def first_name(self) -> str:
        return self.user.first_name
    
    @property
    def last_name(self) -> str:
        return self.user.last_name
    
    def __str__(self) -> str:
        return f'{self.username} ({self.first_name} {self.last_name})'


class SportClient(UUIDMixin, CreatedMixin, ModifiedMixin):
    sport = models.ForeignKey(Sport, verbose_name=_('sport'), on_delete=models.CASCADE)
    cleint = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.CASCADE)

    class Meta:
        db_table = '"crud_api"."sport_client"'
        verbose_name = _('relationship sport client')
        verbose_name_plural = _('relationships sport client')
