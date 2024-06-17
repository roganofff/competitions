"""App config module."""
from django.apps import AppConfig


class CompetitionsAppConfig(AppConfig):
    """Application config class.

    Args:
        AppConfig: Class representing a Django application and its configuration.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'competitions_app'
