"""Module with database models."""
import random
from datetime import datetime, timezone
from uuid import uuid4

from django.conf.global_settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from competitions_app import config

NAME = 'name'
MAX_LENGTH_NAME = 100
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_PLACE = 150
DECIMAL_PLACES = 2
MAX_DIGITS = 5


def get_datetime():
    """Return current datetime.

    Returns:
        datetime: datetime
    """
    return datetime.now(timezone.utc)


def get_random_bet_coefficient():
    """Return random number in diapason.

    Returns:
        float: bet coefficient.
    """
    is_big_coef = random.uniform(0, 1) > config.POINT_SEVEN
    if is_big_coef:
        return round(random.uniform(3, config.TWELVE), 2)
    return round(random.uniform(1, 3), 2)


def check_created(dt: datetime):
    """Check creation date.

    Args:
        dt (datetime): datetime to check

    Raises:
        ValidationError: if given datetime is bigger than current.
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )


def check_modified(dt: datetime):
    """Check modifying date.

    Args:
        dt (datetime): datetime to check.

    Raises:
        ValidationError: if given datetime is bigger than current.
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )


def check_positive(number) -> None:
    """Check if given number is positive.

    Args:
        number: desired number.

    Raises:
        ValidationError: if given number is negative.
    """
    if number < 0:
        raise ValidationError('value should be equal or greater than zero')


class UUIDMixin(models.Model):
    """UUID mixin database model.

    Args:
        models: Django models.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Meta abstract data class."""

        abstract = True


class NameMixin(models.Model):
    """Name mixin database model.

    Args:
        models: Django models.
    """

    name = models.TextField(_(NAME), null=False, blank=False, max_length=MAX_LENGTH_NAME)

    class Meta:
        """Meta abstract data class."""

        abstract = True


class CreatedMixin(models.Model):
    """Creation date database model.

    Args:
        models: Django models.
    """

    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        """Meta data class."""

        abstract = True


class ModifiedMixin(models.Model):
    """Modifying date database model.

    Args:
        models: Django models.
    """

    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_modified],
    )

    class Meta:
        """Modifying meta data class."""

        abstract = True


class Competition(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    """Competition database model.

    Args:
        UUIDMixin: model uuid mixin.
        NameMixin: model name mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        Competition: competition instance.
    """

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

    sports = models.ManyToManyField(
        'Sport',
        verbose_name=_('sports'),
        through='CompetitionsSports',
    )

    @property
    def obj_name(self):
        """Competition abstract name property.

        Returns:
            str: competition name.
        """
        return self.name

    def __str__(self) -> str:
        """Competition string representation.

        Returns:
            str: string object.
        """
        return f'{self.name}: {self.competition_start}—{self.competition_end}.'

    class Meta:
        """Competition meta data class."""

        db_table = '"crud_api"."competition"'
        ordering = ['competition_start', 'competition_end', NAME]
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')
        constraints = [
            models.CheckConstraint(
                check=models.Q(competition_end__gt=models.F('competition_start')),
                name='check_start_date',
                violation_error_message=_('Competition cannot end before its start.'),
            ),
        ]


class Sport(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    """Sport database model.

    Args:
        UUIDMixin: model uuid mixin.
        NameMixin: model name mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        Sport: sport instance.
    """

    description = models.TextField(
        _('description'),
        null=True, blank=True,
        max_length=MAX_LENGTH_DESCRIPTION,
    )

    competitions = models.ManyToManyField(
        Competition,
        verbose_name=_('competitions'),
        through='CompetitionsSports',
    )

    @property
    def obj_name(self):
        """Sport object name.

        Returns:
            str: name of sport.
        """
        return self.name

    def __str__(self) -> str:
        """Sport string representation.

        Returns:
            str: string object.
        """
        return f'{self.name}. {self.description}'

    class Meta:
        """Sport meta data class."""

        db_table = '"crud_api"."sport"'
        ordering = [NAME]
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')


class Stage(UUIDMixin, NameMixin, CreatedMixin, ModifiedMixin):
    """Stage database model.

    Args:
        UUIDMixin: model uuid mixin.
        NameMixin: model name mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        Stage: stage instance.
    """

    stage_date = models.DateField(_('stage_date'), null=False, blank=False, default=get_datetime)
    place = models.TextField(_('place'), null=True, blank=True, max_length=MAX_LENGTH_PLACE)

    bet_coefficient = models.DecimalField(
        _('bet_coefficient'),
        null=False,
        blank=False,
        decimal_places=DECIMAL_PLACES,
        max_digits=MAX_DIGITS,
        default=get_random_bet_coefficient,
    )

    comp_sport = models.ForeignKey(
        'CompetitionsSports',
        verbose_name=_('comp_sport'),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    clients = models.ManyToManyField(
        'Client',
        through='StageClient',
        verbose_name=_('users'),
    )

    def __str__(self) -> str:
        """Stage string representation.

        Returns:
            str: string object.
        """
        return f'{self.name}: {self.place}({self.stage_date}).'

    def clean(self) -> None:
        """Validate bypassing API validation.

        Raises:
            ValidationError: if stage helds before competition.
            ValidationError: if stage helds after competition.

        Returns:
            valid: is valid data.
        """
        if self.stage_date < self.comp_sport.competition_id.competition_start:
            raise ValidationError(_('Stage cannot be held before the competition start.'))
        if self.stage_date > self.comp_sport.competition_id.competition_end:
            raise ValidationError(_('Stage cannot be held after the competition end.'))
        return super().clean()

    class Meta:
        """Stage meta data class."""

        db_table = '"crud_api"."stage"'
        ordering = ['stage_date', NAME]
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')


class CompetitionsSports(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Competitions sports database model.

    Args:
        UUIDMixin: model uuid mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        CompetitionsSports: competition_sport instance.
    """

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
        """CompetitionsSports meta data class."""

        db_table = '"crud_api"."competitions_sports"'
        ordering = ['competition_id', 'sport_id']
        verbose_name = _('relationship competition sports')
        verbose_name_plural = _('relationships competition sports')

    def __str__(self) -> str:
        """Competition sport string representation.

        Returns:
            str: string object.
        """
        return f'{self.competition_id}: {self.sport_id.obj_name}'


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Client database model.

    Args:
        UUIDMixin: model uuid mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        Client: client instance.
    """

    money = models.DecimalField(
        verbose_name=_('money'),
        decimal_places=2,
        max_digits=config.ELEVEN,
        default=0,
        validators=[check_positive],
    )
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        unique=True,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=100, blank=True)
    stages = models.ManyToManyField(Stage, through='StageClient', verbose_name=_('stages'))

    class Meta:
        """Client meta data class."""

        db_table = '"crud_api"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    @property
    def username(self) -> str:
        """Client username property.

        Returns:
            str: username.
        """
        return self.user.username

    @property
    def first_name(self) -> str:
        """Client first name property.

        Returns:
            str: first name.
        """
        return self.user.first_name

    @property
    def last_name(self) -> str:
        """Client last name property.

        Returns:
            str: last name.
        """
        return self.user.last_name

    def __str__(self) -> str:
        """Client representation in string.

        Returns:
            str: string object.
        """
        return f'{self.username} ({self.first_name} {self.last_name})'


class StageClient(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Stage Client database model.

    Args:
        UUIDMixin: model uuid mixin.
        CreatedMixin: model create mixin.
        ModifiedMixin: model modify mixin.

    Returns:
        StageClient: stage client instance.
    """

    stages = models.ForeignKey(Stage, verbose_name=_('stage'), on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.CASCADE)

    class Meta:
        """StageClient meta data class."""

        db_table = '"crud_api"."stage_client"'
        verbose_name = _('relationship stage client')
        verbose_name_plural = _('relationships stage client')
