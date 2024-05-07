from django.contrib.auth import forms, models
from django.forms import Form, CharField, DecimalField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Registration(forms.UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AddFundsForm(Form):
    amount = DecimalField(decimal_places=2, max_digits=8)

    def is_valid(self) -> bool:
        standard_valid = super().is_valid()
        amount = self.cleaned_data.get('amount', None)
        amount_positive = True
        if amount and amount < 0:
            amount_positive = False
            error_list = [ValidationError(_('amount value should be equal or greater than zero'))]
            if self.errors.get('amount'):
                self.errors['amount'] += error_list
            else:
                self.errors['amount'] = error_list
        return standard_valid and amount_positive
