from rest_framework import serializers
from finance.models import PayableTitle, ReceivableTitle


class ReceivableTitleSerializer(serializers.ModelSerializer):
    str_representation = serializers.SerializerMethodField()

    class Meta:
        model = ReceivableTitle
        fields = '__all__'

    def get_str_representation(self, obj):
        return str(obj)


class PayableTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PayableTitle
        fields = '__all__'