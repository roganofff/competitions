"""Module for testing the API."""
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from competitions_app import config
from competitions_app.models import Competition, Sport, Stage

TEST_USERNAME = 'abcdef'
TEST_SUPERUSERNAME = 'admin'


def create_api_test(model, url, creation_attrs):
    """Create test for API.

    Args:
        model (models): database model to test.
        url (str): API endpoint.
        creation_attrs (dict): attributes requiered to create model instance.

    Returns:
        ApiTest: TestCase for Django tests.
    """
    class ApiTest(TestCase):
        def setUp(self) -> None:
            self.client = APIClient()
            self.user = User.objects.create(username=TEST_USERNAME, password=config.TEST_PASSWORD)
            self.superuser = User.objects.create(
                username=TEST_SUPERUSERNAME,
                password=config.TEST_SUPERUSERPASSWORD,
                is_superuser=True,
            )
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def manage(
            self, user: User, token: Token,
            post_expected: int,
            put_expected: int,
            delete_expected: int,
        ):
            self.client.force_authenticate(user=user, token=token)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            response = self.client.post(url, creation_attrs)
            self.assertEqual(response.status_code, post_expected)

            created_id = model.objects.create(**creation_attrs).id
            instance_url = f'{url}{created_id}/'
            put_response = self.client.put(instance_url, creation_attrs)
            self.assertEqual(put_response.status_code, put_expected)

            delete_response = self.client.delete(instance_url, creation_attrs)
            self.assertEqual(delete_response.status_code, delete_expected)

        def test_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_expected=status.HTTP_201_CREATED,
                put_expected=status.HTTP_200_OK,
                delete_expected=status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            self.manage(
                self.user, self.user_token,
                post_expected=status.HTTP_403_FORBIDDEN,
                put_expected=status.HTTP_403_FORBIDDEN,
                delete_expected=status.HTTP_403_FORBIDDEN,
            )
    return ApiTest


competition_attrs = {
    'name': 'abc',
    'competition_start': date(config.TEST_YEAR, 8, 1),
    'competition_end': date(config.TEST_YEAR, 8, 10),
}
sport_attrs = {'name': 'def'}
stage_attrs = {'name': 'ghi', 'stage_date': date(config.TEST_YEAR, 8, 4)}

base_url = '/api/'
CompetitionApiTest = create_api_test(Competition, f'{base_url}competitions/', competition_attrs)
SportApiTest = create_api_test(Sport, f'{base_url}sports/', sport_attrs)
StageApiTest = create_api_test(Stage, f'{base_url}stages/', stage_attrs)
