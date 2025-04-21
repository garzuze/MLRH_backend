from rest_framework import serializers
from finance.models import AccountsReceivableTitle


class AccountsReceivableTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountsReceivableTitle
        fields = '__all__'