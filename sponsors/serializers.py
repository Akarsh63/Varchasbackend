from .models import Sponsor
from rest_framework import serializers


class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'sponsor_type', 'link', 'logo', ]
