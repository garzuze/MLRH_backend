from rest_framework import serializers
from finance.models import AccountsPayableTitle, AccountsReceivableTitle


class AccountsReceivableTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountsReceivableTitle
        fields = '__all__'


class AccountsPayableTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountsPayableTitle
        fields = '__all__'