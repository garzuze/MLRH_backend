from rest_framework import serializers
from .models import Client, Benefit, ClientFee, EconomicActivity, ClientContact, Service


class EconomicActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicActivity
        fields = ["id", "title"]


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ["id", "benefit"]


class ClientSerializer(serializers.ModelSerializer):
    benefits = serializers.PrimaryKeyRelatedField(
        queryset=Benefit.objects.all(), many=True
    )
    economic_activity = serializers.PrimaryKeyRelatedField(
        queryset=EconomicActivity.objects.all()
    )

    class Meta:
        model = Client
        fields = "__all__"


class ClientMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "corporate_name"]


class ClientContactSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = ClientContact
        fields = ["id", "client", "name", "department", "phone", "email", "status"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service"]


class ClientFeeSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = ClientFee
        fields = ["id", "client", "service", "percentual", "value", "deadline"]
