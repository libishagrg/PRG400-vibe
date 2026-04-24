from rest_framework import serializers
from apps.tours.serializers import TourListSerializer
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    tour_detail = TourListSerializer(source='tour', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'created_at', 'updated_at']

    def validate(self, attrs):
        tour_date = attrs.get('tour_date')
        travelers = attrs.get('number_of_travelers', 1)
        if tour_date and tour_date.available_spots < travelers:
            raise serializers.ValidationError(
                f"Only {tour_date.available_spots} spots available for this date."
            )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
