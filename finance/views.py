from rest_framework import permissions, viewsets

from finance.models import AccountsPayableTitle, AccountsReceivableTitle
from finance.serializers import AccountsPayableTitleSerializer, AccountsReceivableTitleSerializer

class AccountsReceivableTitleViewSet(viewsets.ModelViewSet):
    queryset = AccountsReceivableTitle.objects.all()
    serializer_class = AccountsReceivableTitleSerializer
    permission_classes = [permissions.IsAdminUser]


class AccountsPayableTitleViewSet(viewsets.ModelViewSet):
    queryset = AccountsPayableTitle.objects.all()
    serializer_class = AccountsPayableTitleSerializer
    permission_classes = [permissions.IsAdminUser]