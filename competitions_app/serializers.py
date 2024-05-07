from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Competition, Sport, Stage


class CompetitionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = [
            'id', 'competition_start', 'competition_end',
            'created', 'modified',
        ]

class SportSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = [
            'id', 'description',
            'created', 'modified',
        ]

class StageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'id', 'stage_date', 'place',
            'created', 'modified',
        ]