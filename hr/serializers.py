from rest_framework import serializers

from clients.models import Client, ClientContact, ClientFee
from .models import Profile, Resume, Position
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


class ProfileSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_contact = serializers.PrimaryKeyRelatedField(queryset=ClientContact.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    fee = serializers.PrimaryKeyRelatedField(queryset=ClientFee.objects.all())
    str_representation = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_str_representation(self, obj):
        return str(obj)