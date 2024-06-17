"""Module for testing the forms."""
import datetime

from django.test import TestCase

from competitions_app import config
from competitions_app.forms import MakeBetForm, Registration
from tests.app.forms import CardCode, CardExpiry, CardNumber


class TestMakeBetForm(TestCase):
    """Test class for MakeBetForm.

    Args:
        TestCase: test case django class.
    """

    def test_successful(self):
        """Test case for correct data."""
        self.assertTrue(MakeBetForm(data={'bet_amount': 123.45}).is_valid())

    def test_negative(self):
        """Test case for negative bet_amount value."""
        form = MakeBetForm(data={'bet_amount': -123.45})
        self.assertFalse(form.is_valid())

    def test_positive_lt_hundred(self):
        """Test case for positive value lower than hundred."""
        form = MakeBetForm(data={'bet_amount': 23.45})
        self.assertFalse(form.is_valid())


class TestRegistrationForm(TestCase):
    """Test class for Registration form.

    Args:
        TestCase: test case django class.
    """

    _valid_attrs = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        config.PASSWORD1: 'Gnkjhdfj8890',
        config.PASSWORD2: 'Gnkjhdfj8890',
        'email': 'sirius@sirius.ru',
    }
    _not_nullable_fields = ('username', config.PASSWORD1, config.PASSWORD2)

    def test_empty(self):
        """Test case for empty value."""
        for field in self._not_nullable_fields:
            attrs = self._valid_attrs.copy()
            attrs[field] = ''
            self.assertFalse(Registration(data=attrs).is_valid())

    def test_invalid_email(self):
        """Test case for an invalid email address."""
        attrs = self._valid_attrs.copy()
        attrs['email'] = 'Vlad Beznosov'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_different_password(self):
        """Test case for different confirm passwords."""
        attrs = self._valid_attrs.copy()
        attrs[config.PASSWORD1] = 'JHfdshkfdfkhs71239217'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_common_password(self):
        """Test case for too common password."""
        attrs = self._valid_attrs.copy()
        attrs[config.PASSWORD1] = attrs[config.PASSWORD2] = 'Abcde123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_numeric_password(self):
        """Test case for numeric password."""
        attrs = self._valid_attrs.copy()
        attrs[config.PASSWORD1] = attrs[config.PASSWORD2] = '123456789'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_short_password(self):
        """Test case for shprt password."""
        attrs = self._valid_attrs.copy()
        attrs[config.PASSWORD1] = attrs[config.PASSWORD2] = 'ABC123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_successful(self):
        """Test case for successful data input."""
        self.assertTrue(Registration(data=self._valid_attrs).is_valid())


class CardNumberTest(TestCase):
    """Test class for CardNumber form.

    Args:
        TestCase: test case django class.
    """

    def test_input_plain(self):
        """Test case for plain input."""
        form = CardNumber({
            config.NUMBER: '30569309025904',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.NUMBER], '30569309025904')

    def test_input_with_spaces(self):
        """Test case for spaced input."""
        form = CardNumber({
            config.NUMBER: '4111 1111 1111 1111',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.NUMBER], '4111111111111111')

    def test_input_with_dashes(self):
        """Test case for dashed input."""
        form = CardNumber({
            config.NUMBER: '3782-8224631-0005',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.NUMBER], '378282246310005')

    def test_long_input_with_dashes(self):
        """Test case for long cc number with dashes."""
        form = CardNumber({
            config.NUMBER: '4532-2616-1547-6013542',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.NUMBER], '4532261615476013542')

    def test_too_short(self):
        """Test case for too short cc number."""
        form = CardNumber({
            config.NUMBER: '4111 1111 112',
        })
        self.assertFalse(form.is_valid())
        number_error = form.errors[config.NUMBER]
        self.assertEqual(number_error.data[0].code, 'min_length')

    def test_too_long(self):
        """Test case for too long cc number."""
        form = CardNumber({
            config.NUMBER: '4111 1111 1111 1111 1115',
        })
        self.assertFalse(form.is_valid())
        number_error = form.errors[config.NUMBER]
        self.assertEqual(number_error.data[0].code, 'max_length')

    def test_invalid_luhn(self):
        """Test case for invalid luhn algorithm."""
        form = CardNumber({
            config.NUMBER: '4111-1111-1111-1110',
        })
        self.assertFalse(form.is_valid())
        number_error = form.errors[config.NUMBER]
        self.assertEqual(number_error.data[0].code, config.INVALID)


class CardExpiryTest(TestCase):
    """Test class for CardExpiry form.

    Args:
        TestCase: test case django class.
    """

    def test_invalid_string(self):
        """Test case for invalid string."""
        form = CardExpiry({
            config.EXPIRY: '2018-11-10',
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, config.INVALID)

    def test_short_string(self):
        """Test case for short string."""
        form = CardExpiry({
            config.EXPIRY: '07/30',
        })
        self.assertTrue(form.is_valid())
        expiry_error = form.cleaned_data[config.EXPIRY]
        self.assertEqual(expiry_error, datetime.date(config.YEAR_THITRY, 7, config.DAY_LAST))

    def test_invalid_short_string(self):
        """Test case for invalid short string."""
        form = CardExpiry({
            config.EXPIRY: '13/18',
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, config.INVALID)

    def test_long_string(self):
        """Test case for long string."""
        form = CardExpiry({
            config.EXPIRY: '01/2025',
        })
        self.assertTrue(form.is_valid())
        expiry_error = form.cleaned_data[config.EXPIRY]
        self.assertEqual(expiry_error, datetime.date(
            config.YEAR_TWENTY_FIVE,
            1,
            config.DAY_LAST,
            ),
        )

    def test_invalid_long_string(self):
        """Test case for invalid long string."""
        form = CardExpiry({
            config.EXPIRY: '01/200',
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, config.INVALID)

    def test_date_object(self):
        """Test case for date ojbect instead of string."""
        form = CardExpiry({
            config.EXPIRY: datetime.date(config.YEAR_THITRY, config.ELEVEN, 5),
        })
        self.assertTrue(form.is_valid())
        expiry_error = form.cleaned_data[config.EXPIRY]
        self.assertEqual(expiry_error, datetime.date(
            config.YEAR_THITRY,
            config.ELEVEN,
            config.PRE_LAST_DAY,
            ),
        )

    def test_passed_date(self):
        """Test case for passed data."""
        form = CardExpiry({
            config.EXPIRY: '10/09',
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, 'date_passed')

        form = CardExpiry({
            config.EXPIRY: '06/1988',
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, 'date_passed')

        form = CardExpiry({
            config.EXPIRY: datetime.date(config.YEAR_TWENTY_TWELVE, config.ELEVEN, 8),
        })
        self.assertFalse(form.is_valid())
        expiry_error = form.errors[config.EXPIRY]
        self.assertEqual(expiry_error.data[0].code, 'date_passed')

    def test_input_datetime(self):
        """Test cate for datetime as input instead of string."""
        form = CardExpiry({
            config.EXPIRY: datetime.datetime(
                config.YEAR_THITRY,
                config.TWELVE,
                config.FIFTEEN,
                config.TWENTY_THREE,
                config.FIFTY_NINE,
                config.FIFTY_NINE,
            ),
        })
        self.assertTrue(form.is_valid())
        expiry_error = form.cleaned_data[config.EXPIRY]
        self.assertEqual(
            expiry_error,
            datetime.date(
                config.YEAR_THITRY,
                config.TWELVE,
                config.DAY_LAST,
            ),
        )


class CardCodeTest(TestCase):
    """Test class for CardCode form.

    Args:
        TestCase: test case django class.
    """

    def test_input_three_digits(self):
        """Test case for three digit input."""
        form = CardCode({
            config.CODE: '111',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.CODE], '111')

    def test_input_four_digits(self):
        """Test case for four digit input."""
        form = CardCode({
            config.CODE: '1111',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[config.CODE], '1111')

    def test_input_invalid(self):
        """Test case for invalid input."""
        form = CardCode({
            config.CODE: 'abc',
        })
        self.assertFalse(form.is_valid())
        code_errors = form.errors[config.CODE]
        self.assertEqual(code_errors.data[0].code, config.INVALID)

    def test_input_less_than_minimum_lenght(self):
        """Test case for too short input."""
        form = CardCode({
            config.CODE: '66',
        })
        self.assertFalse(form.is_valid())
        code_errors = form.errors[config.CODE]
        self.assertEqual(code_errors.data[0].code, config.INVALID)

    def test_input_more_than_maximum_lenght(self):
        """Test case fot too long input."""
        form = CardCode({
            config.CODE: '66666',
        })
        self.assertFalse(form.is_valid())
        code_errors = form.errors[config.CODE]
        self.assertEqual(code_errors.data[0].code, config.INVALID)
