"""Module for testing utilities."""
from datetime import date

from django.test import TestCase

from competitions_app import config
from competitions_app.utils import expiry_date, luhn


class UtilsTest(TestCase):
    """Test class creating tests.

    Args:
        TestCase: TestCase from django.
    """

    def test_luhn(self):
        """Test Luhn algorithm."""
        valid = [
            '000000018',
            '0000000000000000',
            '2204883716636153',
            '2200111234567898',
            '2200481349288130',
            '30569309025904',
            '3566002020360505',
            '378282246310005',
            '371449635398431',
            '378734493671000',
            '38520000023237',
            '4012888888881881',
            '4111111111111111',
            '4242424242424242',
            '4532261615476013542',
            '5105105105105100',
            '5555555555554444',
            '5610591081018250',
            '6011111111111117',
            '6331101999990016',
        ]
        invalid = [
            '4242424242424240',
            '4242424242424241',
            '4242424242424243',
            '4242424242424244',
            '4242424242424245',
            '4242424242424246',
            '4242424242424247',
            '4242424242424248',
            '4242424242424249',
        ]

        for number in valid:
            with self.subTest(number):
                self.assertTrue(luhn(number))
        for other_number in invalid:
            with self.subTest(other_number):
                self.assertFalse(luhn(other_number))

    def test_expiry_date(self):
        """Test expiry date function."""
        tests = {
            (config.YEAR_TWENTY_FIFTEEN, 6): date(
                config.YEAR_TWENTY_FIFTEEN,
                6,
                config.PRE_LAST_DAY,
            ),
            (config.YEAR_TWENTY_SIXTEEN, 2): date(
                config.YEAR_TWENTY_SIXTEEN,
                2,
                config.TWENTY_NINE,
            ),
            (config.YEAR_TWENTY_EIGHTEEN, 2): date(
                config.YEAR_TWENTY_EIGHTEEN,
                2,
                config.TWENTY_EIGTH,
            ),
            (config.YEAR_TWENTY_EIGHTEEN, 12): date(
                config.YEAR_TWENTY_EIGHTEEN,
                config.TWELVE,
                config.DAY_LAST,
            ),
            (config.YEAR_TWENTY_TWO, 9): date(config.YEAR_TWENTY_TWO, 9, config.PRE_LAST_DAY),
        }
        for (year, month), days in tests.items():
            with self.subTest('{}-{}'.format(year, month)):
                self.assertEqual(expiry_date(year, month), days)
