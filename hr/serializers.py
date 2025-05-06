from rest_framework import serializers, exceptions

from clients.models import Client, ClientContact, ClientFee
from .models import Profile, Report, Resume, Position, WorkExperience
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkExperienceSerializer(serializers.ModelSerializer):
    resume = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all(), many=False
    )

    class Meta:
        model = WorkExperience
        fields = "__all__"
        read_only_fields = ("resume",)
    
    def validate(self, data):
        user = self.context["request"].user
        expected_resume = Resume.objects.filter(user=user).first()
        payload_resume = data["resume"]

        # Usuário não tem um currículo e não é admin
        if not expected_resume and not user.is_superuser:
            raise exceptions.AuthenticationFailed

        if expected_resume:
        # Usuário não é admin e tentou alterar um currículo que não é seu
            if not user.is_superuser and expected_resume != payload_resume:
                raise exceptions.AuthenticationFailed

        return data
    
    def get_user_data(self, obj):
        return [obj.resume.user.email, obj.resume.user.cpf]


class ResumeSerializer(serializers.ModelSerializer):
    desired_positions = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), many=True
    )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    availability = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    positions_str = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_availability(self, obj):
        return obj.availability()

    def get_age(self, obj):
        return obj.age()

    def get_positions_str(self, obj):
        return obj.positions_str()

    def get_user_data(self, obj):
        return {"email": obj.user.email, "cpf": obj.user.cpf}


class SlimResumeSerializer(ResumeSerializer):
    """Reduced Resume Serializer for working with Resume tables"""
    work_experiences = WorkExperienceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Resume
        fields = [
            "id",
            "name",
            "phone",
            "expected_salary",
            "neighborhood",
            "city",
            "age",
            "positions_str",
            "updated_at",
            "desired_positions",
            "work_experiences"
        ]

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_contact = serializers.PrimaryKeyRelatedField(
        queryset=ClientContact.objects.all()
    )
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    fee = serializers.PrimaryKeyRelatedField(queryset=ClientFee.objects.all())
    location = serializers.SerializerMethodField()
    position_str = serializers.SerializerMethodField()
    benefits = serializers.SerializerMethodField()
    client_description = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_location(self, obj):
        return obj.location()

    def get_position_str(self, obj):
        return obj.position.title

    def get_benefits(self, obj):
        return obj.client_benefits()

    def get_client_description(self, obj):
        return obj.client.description


class ReportSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())
    str_representation = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = "__all__"

    def get_str_representation(self, obj):
        return str(obj)
