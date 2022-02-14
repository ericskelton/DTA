from rest_framework import serializers
from .models import Detectives

class DetectiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detectives
        fields = ('id', 'name', 'location')