"""Testing forms module."""
from django import forms as dj_forms

from competitions_app import forms


class CardNumber(dj_forms.Form):
    """Test credit card number form.

    Args:
        forms (dj_forms.Form): A collection of Fields, plus their associated data.
    """

    number = forms.CardNumberField()


class CardExpiry(dj_forms.Form):
    """Test credit card expiration date form.

    Args:
        forms (dj_forms.Form): A collection of Fields, plus their associated data.
    """

    expiry = forms.CardExpiryField()


class CardCode(dj_forms.Form):
    """Test credit card number form.

    Args:
        forms (dj_forms.Form): A collection of Fields, plus their associated data.
    """

    code = forms.SecurityCodeField()
