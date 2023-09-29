from registration.models import TeamRegistration
from .models import BasketBall, Cricket, Football, Match, Volleyball, Chess, Squash, Badminton, TT, Tennis
from rest_framework import serializers


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:match-detail")
    team1 = serializers.SlugRelatedField(queryset=TeamRegistration.objects.all(), slug_field="teamId")
    team2 = serializers.SlugRelatedField(queryset=TeamRegistration.objects.all(), slug_field="teamId")

    class Meta:
        model = Match
        fields = ['url', 'event', 'event_id', 'team1', 'team2', 'venue', 'date', 'time']


class CricketSerializer(serializers.HyperlinkedModelSerializer):
    # url = url = serializers.HyperlinkedIdentityField(view_name="events:match-detail")
    url = serializers.HyperlinkedIdentityField(view_name="events:cricket-detail")
    # url = serializers.HyperlinkedIdentityField(view_name="events:match-detail")
    match = serializers.SlugRelatedField(queryset=Match.objects.all().filter(event='5'), slug_field="event_id")
    # match = MatchSerializer()

    class Meta:
        model = Cricket
        fields = ['url', 'match', 'run1', 'run2', 'wicket1', 'wicket2', 'overs1', 'overs2']


class FootballSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:football-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='6'))

    class Meta:
        model = Football
        fields = ['url', 'match', 'score1', 'score2', ]


class VolleyballSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:volleyball-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='9'))

    class Meta:
        model = Volleyball
        fields = ['url', 'match', 'score1', 'score2', 'setNo']


class ChessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chess
        fields = ['match', 'score1', 'score2', ]


class SquashSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Squash
        fields = ['match', 't1s1', 't2s1', 't1s2', 't2s2', 't1s3', 't2s3', 't1s4', 't2s4', 't1s5', 't2s5', 't1sw', 't2sw']


class BadmintonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:badminton-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='2'))

    class Meta:
        model = Badminton
        fields = ['url', 'match', 't1s1', 't2s1', 't1s2', 't2s2', 't1s3', 't2s3', 't1sw', 't2sw']


class TTSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:TT-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='7'))

    class Meta:
        model = TT
        fields = ['url', 'match', 't1s1', 't2s1', 't1s2', 't2s2', 't1s3', 't2s3', 't1sw', 't2sw']


class TennisSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:Tennis-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='8'))

    class Meta:
        model = Tennis
        fields = ['url', 'match', 't1s1', 't2s1', 't1s2', 't2s2', 't1s3', 't2s3', 't1sw', 't2sw']


class BasketballSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:Basketball-detail")
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all().filter(event='2'))

    class Meta:
        model = BasketBall
        fields = ['url', 'match', 't1q1', 't2q1', 't1q2', 't2q2', 't1q3', 't2q3', 't1q4', 't2q4']
