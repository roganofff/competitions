"""Module for validators."""
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import utils


@deconstructible
class CCNumberValidator:
    """Credit Card Nummber validator.

    Raises:
        ValidationError: An error while validating data about cc number.

    Returns:
        bool: is cc number valid.
    """

    message = _('Enter a valid credit card number.')
    message_code = 'invalid'

    def __init__(self, message=None, code=None):
        """Initialize the validator.

        Args:
            message (str, optional): text message. Defaults to None.
            code (str, optional): output code. Defaults to None.
        """
        if message is not None:
            self.msg = message
        if code is not None:
            self.msg_code = code

    def __call__(self, field):
        """On call function validate.

        Args:
            field: value to validate

        Raises:
            ValidationError: error if validate fails.
        """
        if not utils.luhn(utils.get_digits(field)):
            raise ValidationError(self.message, code=self.message_code)

    def __eq__(self, other):
        """Are two objects equal.

        Args:
            other: object to compare.

        Returns:
            bool: if objects are equal.
        """
        return (
            isinstance(other, self.__class__) and
            (self.message == other.message) and
            (self.code == other.code)
        )


@deconstructible
class CSCValidator(RegexValidator):
    """Credit Card CSCV validator.

    Raises:
        ValidationError: An error while validating data about CSCV number.

    Returns:
        bool: is CSCV number valid.
    """

    regex = r'^\d{3,4}$'
    message = _('Enter a valid security code.')
    code = 'invalid'


@deconstructible
class ExpiryDateValidator:
    """Credit Card Expiry Date validator.

    Raises:
        ValidationError: An error while validating data about cc expiry.

    Returns:
        bool: is cc expired.
    """

    msg = _('This date has passed.')
    msg_code = 'date_passed'

    def __init__(self, message=None, code=None):
        """Initialize the validator.

        Args:
            message (str, optional): text message. Defaults to None.
            code (str, optional): output code. Defaults to None.
        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, field):
        """On call function validate.

        Args:
            field: value to validate

        Raises:
            ValidationError: error if validate fails.
        """
        expiry_date = utils.expiry_date(field.year, field.month)
        if expiry_date < datetime.date.today():
            raise ValidationError(self.msg, code=self.msg_code)

    def __eq__(self, other):
        """Are two objects equal.

        Args:
            other: object to compare.

        Returns:
            bool: if objects are equal.
        """
        return (
            isinstance(other, self.__class__)
            and (self.message == other.message)
            and (self.code == other.code)
        )
