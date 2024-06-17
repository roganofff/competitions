import datetime 
from django.contrib.auth import forms, models
from django.forms import DateField, Form, CharField, DecimalField, PasswordInput
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from .widgets import ExpiryDateWidget, TelephoneInput

from .validators import CCNumberValidator, CSCValidator, ExpiryDateValidator

from . import utils


class Registration(forms.UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(Form):
    """
    Form for logging in a user.

    This form allows the user to enter their username and password and log in.
    The username must exist in the database and the password must be correct.

    Attributes:
        username (CharField): ACharField for entering a username.
        password (CharField): ACharField for entering a password.
    """

    username = CharField(label='Login')
    password = CharField(label='Password', widget=PasswordInput)

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


class CardNumberField(CharField):
    widget = TelephoneInput
    default_validators = [
        MinLengthValidator(12),
        MaxLengthValidator(19),
        CCNumberValidator(),
    ]

    def to_python(self, value):
        return utils.get_digits(super().to_python(value))

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'[-\d\s]*',
            'autocomplete': 'cc-number',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs


class CardExpiryField(DateField):
    widget = ExpiryDateWidget
    input_formats = ['%m/%y', '%m/%Y']
    default_validators = [ExpiryDateValidator()]

    def prepare_value(self, value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.strftime('%m/%y')
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, datetime.date):
            value = utils.expiry_date(value.year, value.month)
        return value

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d+/\d+',
            'placeholder': 'MM/YY',
            'autocomplete': 'cc-exp',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs


class SecurityCodeField(CharField):
    widget = TelephoneInput
    default_validators = [CSCValidator()]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d*',
            'autocomplete': 'cc-csc',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs


class AddFundsForm(Form):
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')
    amount = DecimalField(decimal_places=2, max_digits=8)

    def is_valid(self) -> bool:
        standard_valid = super().is_valid()
        amount = self.cleaned_data.get('amount')
        cc_number = self.cleaned_data.get('cc_number')
        cc_expiry = self.cleaned_data.get('cc_expiry')
        cc_code = self.cleaned_data.get('cc_code')
        amount_positive = True
        if amount and amount < 0:
            amount_positive = False
            error_list = [_('amount value should be equal or greater than zero')]
            if self.errors.get('Amount'):
                self.errors['Amount'] += error_list
            else:
                self.errors['Amount'] = error_list
        

        return standard_valid and amount_positive
    