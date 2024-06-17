"""Moduel for testing views."""
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from rest_framework import status

from competitions_app import config, models


def create_successful_page_test(page_url, page_name, template, auth=True):
    """Create successful page tests.

    Args:
        page_url (str): path to the url.
        page_name (str): name of the page.
        template (str): template used by page.
        auth (bool, optional): is user authenticated. Defaults to True.

    Returns:
        test: test of the page.
    """
    def test(self):
        self.client = Client()
        if auth:
            user = User.objects.create(
                username=config.TEST_USERNAME,
                password=config.TEST_PASSWORD,
            )
            models.Client.objects.create(user=user)
            self.client.force_login(user)

        reversed_url = reverse(page_name)
        if page_name == 'bet':
            stage = models.Stage.objects.create(
                name='name',
                stage_date=date(config.TEST_YEAR, 8, 4),
            )
            url, reversed_url = f'{page_url}?id={stage.id}', f'{reversed_url}?id={stage.id}'
        else:
            url = page_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTemplateUsed(response, template)

        response = self.client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    return test


def create_redirect_page_test(page_name):
    """Create redirect pages tests.

    Args:
        page_name (str): name of the page.

    Returns:
        test: test of the page.
    """
    def test(self):
        self.client = Client()
        self.client.logout()

        self.assertEqual(self.client.get(reverse(page_name)).status_code, status.HTTP_302_FOUND)

    return test


auth_pages = (
    ('/competitions/', 'competitions', 'catalog/competitions.html'),
    ('/sports/', 'sports', 'catalog/sports.html'),
    ('/stages/', 'stages', 'catalog/stages.html'),
    ('/competition/', 'competition', 'entities/competition.html'),
    ('/sport/', 'sport', 'entities/sport.html'),
    ('/stage/', 'stage', 'entities/stage.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
    ('/bet/', 'bet', 'pages/bet.html'),
)

casual_pages = (
    ('/register/', 'register', 'registration/register.html'),
    ('', 'homepage', 'index.html'),
    ('/login/', 'login', 'registration/login.html'),
)

casual_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in casual_pages}
TestCasualPages = type('TestCasualPages', (TestCase,), casual_methods)

auth_pages_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in auth_pages}
TestAuthPages = type('TestAuthPages', (TestCase,), auth_pages_methods)

no_auth_pages_methods = {
    f'test_{page}': create_redirect_page_test(page) for _, page, _ in auth_pages
}
TestNoAuthPages = type('TestNoAuthPages', (TestCase,), no_auth_pages_methods)
