from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Competition, Sport, Stage


class CompetitionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'competition_start', 'competition_end', 'sports',
            'created', 'modified'
        ]

class SportSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = [
            'id', 'name', 'description', 'competitions',
            'created', 'modified'
        ]

class StageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'id', 'name', 'place', 'stage_date',
            'created', 'modified'
        ]