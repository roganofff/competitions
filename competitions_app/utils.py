"""Module for utilities."""
import calendar
import datetime
import re

LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
re_non_digits = re.compile(r'[^\d]+')


def get_digits(field):
    """Get all digits from input string.

    Args:
        field: str.

    Returns:
        rtype: str.
    """
    if not field:
        return ''
    return re_non_digits.sub('', str(field))


def luhn(number):
    """Validate credit card number with Luhn's Algorithm.

    Args:
        number: str.

    Returns:
        rtype: bool.
    """
    number = str(number)
    try:
        evens = sum(int(ch) for ch in number[-1::-2])
        odds = sum(LUHN_ODD_LOOKUP[int(ch)] for ch in number[-2::-2])
        return (evens + odds) % 10 == 0
    except ValueError:
        return False


def expiry_date(year, month):
    """Return the last day of month.

    Args:
        year: int.
        month: int.

    Returns:
        date: datetime.date
    """
    weekday, day_count = calendar.monthrange(year, month)
    return datetime.date(year, month, day_count)
