from rest_framework import serializers
from .models import Client, Benefit, EconomicActivity, ClientContact

class EconomicActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicActivity
        fields = ['id', 'title']

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ['id', 'benefit']

class ClientSerializer(serializers.ModelSerializer):
    benefits = serializers.PrimaryKeyRelatedField(queryset=Benefit.objects.all(), many=True)
    economic_activity = serializers.PrimaryKeyRelatedField(queryset=EconomicActivity.objects.all())

    class Meta:
        model = Client
        fields = [
            'id', 'corporate_name', 'trade_name', 'cnpj', 'cep', 'address',
            'neighborhood', 'city', 'state', 'state_registration', 'number_of_employees',
            'economic_activity', 'benefits'
        ]


class ClientMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'corporate_name']


class ClientContactSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = ClientContact
        fields = ["id", "client", "name", "department", "phone", "email", "status"]