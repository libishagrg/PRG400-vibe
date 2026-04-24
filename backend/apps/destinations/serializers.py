from rest_framework import serializers
from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    highlight_list = serializers.ReadOnlyField()
    continent_display = serializers.CharField(source='get_continent_display', read_only=True)

    class Meta:
        model = Destination
        fields = '__all__'
