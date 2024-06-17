"""Widget module."""
from django.forms import widgets


class TelephoneInput(widgets.TextInput):
    """TelephoneInput widget.

    Args:
        widgets (TextInput): text input for widget.
    """

    input_type = 'tel'


class ExpiryDateWidget(widgets.TextInput):
    """ExpiryDate widget.

    Args:
        widgets (TextInput): text input for widget.
    """

    pass
