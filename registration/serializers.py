from .models import TeamRegistration
from rest_framework import serializers


class TeamsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="registration:teamregistration-detail")

    class Meta:
        model = TeamRegistration
        fields = ['url', 'teamId', 'college', 'sport', 'score']
