from rest_framework import serializers
from finance.models import AccountsPayableTitle, AccountsReceivableTitle


class AccountsReceivableTitleSerializer(serializers.ModelSerializer):
    str_representation = serializers.SerializerMethodField()

    class Meta:
        model = AccountsReceivableTitle
        fields = '__all__'

    def get_str_representation(self, obj):
        return str(obj)


class AccountsPayableTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountsPayableTitle
        fields = '__all__'