from datetime import date, datetime, timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from competitions_app import models


valid_attrs = {
    'competition': {
        'name': 'abc',
        'competition_start': date(1936, 8, 1),
        'competition_end': date(1936, 8, 16),
    },
    'sport': {'name': 'def'},
    'stage': {'name': 'ghi', 'stage_date': date(1936, 8, 4)},
}

def create_model_tests(model_class, creation_attrs):
    class ModelTest(TestCase):
        def test_successful_creation(self):
            model_class.objects.create(**creation_attrs)
    return ModelTest

CompetitionModelTest = create_model_tests(models.Competition, valid_attrs.get('competition'))
SportModelTest = create_model_tests(models.Sport, valid_attrs.get('sport'))
StageModelTest = create_model_tests(models.Stage, valid_attrs.get('stage'))

class TestLinks(TestCase):
    def test_competitionssports(self):
        competition = models.Competition.objects.create(**valid_attrs.get('competition'))
        sport = models.Sport.objects.create(**valid_attrs.get('sport'))
        competition.sports.add(sport)
        competition.save()
        competitionsport_link = models.CompetitionsSports.objects.filter(
            competition=competition,
            sport=sport,
        )
        self.assertEqual(len(competitionsport_link), 1)

    # def test_bookclient(self):
    #     user = User.objects.create(username='user', password='user')
    #     client = models.Client.objects.create(user=user)
    #     book = models.Book.objects.create(**valid_attrs.get('book'))
    #     client.books.add(book)
    #     client.save()
    #     bookclient_link = models.BookClient.objects.filter(book=book, client=client)
    #     self.assertEqual(len(bookclient_link), 1)

valid_tests = (
    (models._check_created, datetime(2007, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models._check_modified, datetime(2007, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models._check_positive, 1),
)
invalid_tests = (
    (models._check_created, datetime(3000, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models._check_modified, datetime(3000, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models._check_positive, -1),
)

def create_validation_test(validator, value, valid=True):
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _: validator(value) if valid else test

invalid_methods = {
    f'test_invalid_{args[0].__name__}': create_validation_test(*args, False) for args in invalid_tests
}
valid_methods = {
    f'test_valid_{args[0].__name__}': create_validation_test(*args) for args in valid_tests
}
TestValidators = type('TestValidators', (TestCase,), invalid_methods | valid_methods)
