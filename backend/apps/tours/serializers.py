from rest_framework import serializers
from apps.destinations.serializers import DestinationSerializer
from .models import Tour, TourDate


class TourDateSerializer(serializers.ModelSerializer):
    is_sold_out = serializers.ReadOnlyField()

    class Meta:
        model = TourDate
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    destination_detail = DestinationSerializer(source='destination', read_only=True)
    available_dates = TourDateSerializer(many=True, read_only=True)
    discounted_price = serializers.ReadOnlyField()
    includes_list = serializers.ReadOnlyField()
    excludes_list = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'


class TourListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    discounted_price = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'title', 'destination', 'destination_name', 'destination_country',
                  'category', 'category_display', 'difficulty', 'duration_days',
                  'price_per_person', 'discount_percent', 'discounted_price',
                  'image_url', 'rating', 'total_reviews', 'is_featured']
