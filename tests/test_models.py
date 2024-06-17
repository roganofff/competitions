"""Module for testing Django models."""
from datetime import date, datetime, timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from competitions_app import config, models

valid_attrs = {
    'competition': {
        'name': 'abc',
        'competition_start': date(config.TEST_YEAR, 8, 1),
        'competition_end': date(config.TEST_YEAR, 8, config.SIXTEEN),
    },
    'sport': {'name': 'def'},
    'stage': {'name': 'ghi', 'stage_date': date(config.TEST_YEAR, 8, 4)},
}


def create_model_tests(model_class, creation_attrs):
    """Create models for tests.

    Args:
        model_class (models): models for testing.
        creation_attrs (dict[str, Any]): attributes for creation of models.

    Returns:
        ModelTest: TestCase from Django.
    """
    class ModelTest(TestCase):
        """Test case for models instances.

        Args:
            TestCase: TestCase from Django.
        """

        def test_successful_creation(self):
            """Test creation of models successfully."""
            model_class.objects.create(**creation_attrs)
    return ModelTest


CompetitionModelTest = create_model_tests(models.Competition, valid_attrs.get('competition'))
SportModelTest = create_model_tests(models.Sport, valid_attrs.get('sport'))
StageModelTest = create_model_tests(models.Stage, valid_attrs.get('stage'))


class TestDefaultGenerators(TestCase):
    """Test case for default values generators.

    Args:
        TestCase: TestCase from Django.
    """

    def test_get_datetime(self):
        """Test datetime function."""
        datetime_result = models.get_datetime()
        assert isinstance(datetime_result, datetime)

    def test_get_random_bet_coefficient(self):
        """Test random coefficient number function."""
        random_coeff = models.get_random_bet_coefficient()
        assert isinstance(random_coeff, float)
        assert 1 <= random_coeff <= config.TWELVE


class TestLinks(TestCase):
    """Test case for models links.

    Args:
        TestCase: TescCase from Django.
    """

    def test_competitionssports(self):
        """Test competitions sports link."""
        competition = models.Competition.objects.create(**valid_attrs.get('competition'))
        sport = models.Sport.objects.create(**valid_attrs.get('sport'))
        competition.sports.add(sport)
        competition.save()
        competitionsport_link = models.CompetitionsSports.objects.filter(
            competition_id=competition,
            sport_id=sport,
        )
        self.assertEqual(len(competitionsport_link), 1)

    def test_stageslient(self):
        """Test stages client link."""
        user = User.objects.create(username='user', password=config.TEST_USERNAME)
        client = models.Client.objects.create(user=user)
        stage = models.Stage.objects.create(**valid_attrs.get('stage'))
        client.stages.add(stage)
        client.save()
        stageclient_link = models.StageClient.objects.filter(stages=stage, client=client)
        self.assertEqual(len(stageclient_link), 1)


valid_tests = (
    (models.check_created, datetime(config.PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(config.PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_positive, 1),
)
invalid_tests = (
    (models.check_created, datetime(config.NEVER_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(config.NEVER_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_positive, -1),
)


def create_valid_test(validator, fields, valid=True):
    """Create validation test for checker.

    Args:
        validator (Callable): checks and validates the fields.
        fields (Any): being validated.
        valid (bool, optional): True if is valid, False if is not. Defaults to True.

    Returns:
        bool: True if is valid, False if is not.
    """
    def test(self):
        with self.assertRaises(ValidationError):
            validator(fields)
    return lambda _: validator(fields) if valid else test


invalid_methods = {
    f'test_invalid_{args[0].__name__}': create_valid_test(*args, valid=False)
    for args in invalid_tests
}
valid_methods = {
    f'test_valid_{args[0].__name__}': create_valid_test(*args) for args in valid_tests
}
TestValidators = type('TestValidators', (TestCase,), invalid_methods | valid_methods)
