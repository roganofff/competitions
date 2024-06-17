"""Module for testing the adding of funds to the user."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client as DjangoTestClient

from competitions_app import config
from competitions_app.models import Client


class TestAddFunds(TestCase):
    """Testing class for add funds form.

    Args:
        TestCase: test case django class.
    """

    _url = '/profile/'

    client: Client
    api_client: DjangoTestClient
    user: User

    def setUp(self):
        """Set up the user-client."""
        self.user = User.objects.create(username='user', password=config.TEST_USERNAME)
        self.client = Client.objects.create(user=self.user, money=0)
        self.api_client = DjangoTestClient()
        self.api_client.force_login(self.user)

    def test_negative_money(self):
        """Test case for negative money input."""
        self.api_client.post(self._url, {'amount': -1})
        self.client.refresh_from_db()
        self.assertEqual(self.client.money, 0)

    def test_successful(self):
        """Test case for successful data input."""
        self.api_client.post(
            self._url,
            {
                'cc_number': '4242 4242 4242 4242',
                'cc_expiry': '7/30',
                'cc_code': '111',
                'amount': 1,
            },
        )
        self.client.refresh_from_db()
        self.assertEqual(self.client.money, 1)
