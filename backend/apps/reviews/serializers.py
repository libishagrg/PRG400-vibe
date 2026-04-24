from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    tour_title = serializers.CharField(source='tour.title', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'is_verified', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    def validate(self, attrs):
        request = self.context.get('request')
        tour = attrs.get('tour')
        if request and tour:
            if Review.objects.filter(user=request.user, tour=tour).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError('You have already reviewed this tour.')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
