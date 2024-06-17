"""Module for API serializers."""
from rest_framework.serializers import HyperlinkedModelSerializer

from competitions_app import config

from .models import Competition, CompetitionsSports, Sport, Stage


class CompetitionSerializer(HyperlinkedModelSerializer):
    """Competition serializer.

    Args:
        HyperlinkedModelSerializer: link to the model.
    """

    class Meta:
        """Meta data for competition serializer."""

        model = Competition
        fields = config.ALL


class SportSerializer(HyperlinkedModelSerializer):
    """Sport serializer.

    Args:
        HyperlinkedModelSerializer: link to the model.
    """

    class Meta:
        """Meta data for sport serializer."""

        model = Sport
        fields = config.ALL


class StageSerializer(HyperlinkedModelSerializer):
    """Stage serializer.

    Args:
        HyperlinkedModelSerializer: link to the model.
    """

    class Meta:
        """Meta data for stage serializer."""

        model = Stage
        fields = config.ALL


class CompetitionsSportsSerializer(HyperlinkedModelSerializer):
    """Competition Sports serializer.

    Args:
        HyperlinkedModelSerializer: link to the model.
    """

    class Meta:
        """Meta data for competitions sports serializer."""

        model = CompetitionsSports
        fields = config.ALL
