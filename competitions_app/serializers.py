from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Competition, Sport, Stage, CompetitionsSports


class CompetitionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'

class SportSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'

class StageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class CompetitionsSportsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CompetitionsSports
        fields = '__all__'
