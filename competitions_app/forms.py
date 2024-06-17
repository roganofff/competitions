"""Forms module."""
import datetime

from django import forms as dj_form
from django.contrib.auth import forms, models
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from competitions_app import config

from . import utils
from .validators import CCNumberValidator, CSCValidator, ExpiryDateValidator
from .widgets import ExpiryDateWidget, TelephoneInput


class MakeBetForm(dj_form.Form):
    """Betting form.

    Args:
        Form: Forms module.
    """

    bet_amount = dj_form.DecimalField(
        decimal_places=config.DIGIT_PLACES,
        max_digits=config.MONEY_MAX_DIGITS,
    )

    def is_valid(self) -> bool:
        """Validate the form.

        Returns:
            bool: True if the form is valid, False if is not.
        """
        standard_valid = super().is_valid()
        bet_amount = self.cleaned_data.get('bet_amount')
        bet_amount_valid = True
        if bet_amount < 100:
            bet_amount_valid = False
            error_list = [_('amount value should be equal or greater than a hundred')]
            if self.errors.get('Bet amount'):
                self.errors['Bet amount'] += error_list
            else:
                self.errors['Bet amount'] = error_list

        return standard_valid and bet_amount_valid


class Registration(forms.UserCreationForm):
    """Registation form.

    Args:
        forms (UserCreationForm): base for the registration form.
    """

    first_name = dj_form.CharField(max_length=100, required=True)
    last_name = dj_form.CharField(max_length=100, required=True)
    email = dj_form.CharField(max_length=100, required=True)

    class Meta:
        """Class for meta data and fields."""

        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(dj_form.Form):
    """
    Form for logging in a user.

    This form allows the user to enter their username and password and log in.
    The username must exist in the database and the password must be correct.

    Attributes:
        username (CharField): ACharField for entering a username.
        password (CharField): ACharField for entering a password.
    """

    username = dj_form.CharField(label='Login')
    password = dj_form.CharField(label='Password', widget=dj_form.PasswordInput)

    def clean(self):
        """
        Validate the username and password.

        This method validates the username and password entered by the user.
        It checks that the username exists in the database and that the password
        is correct. If the username and password are valid, it sets the user's
        token and saves the user.

        Returns:
            dict: The cleaned data.
        """
        cleaned_data = super().clean()
        self.validate_username_and_password(cleaned_data)
        return cleaned_data

    def validate_username_and_password(self, cleaned_data):
        """
        Validate the username and password.

        This method validates the username and password entered by the user.
        It checks that the username exists in the database and that the password
        is correct. If the username and password are valid, it sets the user's
        token and saves the user.

        Args:
            cleaned_data (dict): The cleaned data.
        """
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.validate_user(username, password)

    def validate_user(self, username, password):
        """
        Validate the user.

        This method validates the user entered by the user. It checks that the
        user exists in the database and that the password is correct. If the
        user and password are valid, it sets the user's token and saves the user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Raises:
            ValidationError: If the user does not exist or the password is incorrect.
        """
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise ValidationError('User with this username was not found.')

        if not user.check_password(password):
            raise ValidationError('Incorrect username of password..')

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        user.save()


class CardNumberField(dj_form.CharField):
    """Credit card number field.

    Args:
        CharField: Forms module.
    """

    widget = TelephoneInput
    default_validators = [
        MinLengthValidator(config.MINLENGTHVALIDATOR),
        MaxLengthValidator(config.MAXLENGTHVALIDATOR),
        CCNumberValidator(),
    ]

    def to_python(self, field):
        """Translate field to python.

        Args:
            field: field to translate.

        Returns:
            str: all digits from input string.
        """
        return utils.get_digits(super().to_python(field))

    def widget_attrs(self, widget):
        """Gather attributes for widget.

        Args:
            widget (TelephoneInput): telephone input.

        Returns:
            dict[str, str]: widget attributes.
        """
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'[-\d\s]*',
            'autocomplete': 'cc-number',
            'autocorrect': config.OFF,
            'spellcheck': config.OFF,
            'autocapitalize': config.OFF,
        })
        return attrs


class CardExpiryField(dj_form.DateField):
    """Credit card expiration date field.

    Args:
        DateField: Forms module.
    """

    widget = ExpiryDateWidget
    input_formats = ['%m/%y', '%m/%Y']
    default_validators = [ExpiryDateValidator()]

    def prepare_value(self, field):
        """Set the value to correct form.

        Args:
            field: field to change.

        Returns:
            str: new form of value.
        """
        if isinstance(field, (datetime.date, datetime.datetime)):
            return field.strftime('%m/%y')
        return field

    def to_python(self, field):
        """Translate field to python.

        Args:
            field: field to translate.

        Returns:
            str: all digits from input string.
        """
        field = super().to_python(field)
        if isinstance(field, datetime.date):
            field = utils.expiry_date(field.year, field.month)
        return field

    def widget_attrs(self, widget):
        """Gather attributes for widget.

        Args:
            widget (TelephoneInput): telephone input.

        Returns:
            dict[str, str]: widget attributes.
        """
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d+/\d+',
            'placeholder': 'MM/YY',
            'autocomplete': 'cc-exp',
            'autocorrect': config.OFF,
            'spellcheck': config.OFF,
            'autocapitalize': config.OFF,
        })
        return attrs


class SecurityCodeField(dj_form.CharField):
    """Credit card security code field.

    Args:
        CharField: Forms module.
    """

    widget = TelephoneInput
    default_validators = [CSCValidator()]

    def widget_attrs(self, widget):
        """Gather attributes for widget.

        Args:
            widget (TelephoneInput): telephone input.

        Returns:
            dict[str, str]: widget attributes.
        """
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d*',
            'autocomplete': 'cc-csc',
            'autocorrect': config.OFF,
            'spellcheck': config.OFF,
            'autocapitalize': config.OFF,
        })
        return attrs


class AddFundsForm(dj_form.Form):
    """Adding funds form.

    Args:
        Form: Forms module.
    """

    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')
    amount = dj_form.DecimalField(decimal_places=2, max_digits=8)

    def is_valid(self) -> bool:
        """Validate the form.

        Returns:
            bool: True if the form is valid, False if is not.
        """
        standard_valid = super().is_valid()
        amount = self.cleaned_data.get('amount')
        amount_positive = True
        if amount and amount < 0:
            amount_positive = False
            error_list = [_('amount value should be equal or greater than zero')]
            if self.errors.get('Amount'):
                self.errors['Amount'] += error_list
            else:
                self.errors['Amount'] = error_list

        return standard_valid and amount_positive
