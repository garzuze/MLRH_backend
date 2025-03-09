from rest_framework import serializers
from .models import Resume, Position
from django.contrib.auth import get_user_model

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    desired_positions = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'