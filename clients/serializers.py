from rest_framework import serializers
from .models import Client, Benefit, EconomicActivity

class EconomicActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EconomicActivity
        fields = ['id', 'title']

class BenefitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Benefit
        fields = ['id', 'benefit']

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    benefits = BenefitSerializer(many=True)
    economic_activity = EconomicActivitySerializer()
    class Meta:
        model = Client
        fields = ['id', 'corporate_name', 'trade_name', 'cnpj', 'cep','address', 'neighborhood', 'city', 'state', 'state_registration', 'number_of_employees', 'economic_activity', 'benefits']