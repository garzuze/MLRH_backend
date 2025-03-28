from rest_framework import serializers

from clients.models import Client, ClientContact, ClientFee
from .models import Profile, Report, Resume, Position, WorkExperience
from django.contrib.auth import get_user_model

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    desired_positions = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    availability = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_availability(self, obj):
        return obj.availability()

    def get_age(self, obj):
        return obj.age()


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_contact = serializers.PrimaryKeyRelatedField(queryset=ClientContact.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    fee = serializers.PrimaryKeyRelatedField(queryset=ClientFee.objects.all())
    location = serializers.SerializerMethodField()
    position_str = serializers.SerializerMethodField()
    benefits = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_location(self, obj):
        return obj.location()
    
    def get_position_str(self, obj):
        return obj.position.title
    
    def get_benefits(self, obj):
        return obj.client_benefits()
        

class ReportSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())
    str_representation = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = '__all__'

    def get_str_representation(self, obj):
        return str(obj)
    

class WorkExperienceSerializer(serializers.ModelSerializer):
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all(), many=False)
    resume = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ('resume', )
    
    def create(self, validated_data):
        user = self.context['request'].user
        resume = Resume.objects.filter(user=user).first()
        validated_data['resume'] = resume
        return super().create(validated_data)