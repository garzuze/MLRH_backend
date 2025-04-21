from django.shortcuts import render
from rest_framework import permissions, viewsets, status

from finance.models import AccountsReceivableTitle
from finance.serializers import AccountsReceivableTitleSerializer

# Create your views here.

class AccountsReceivableTitleViewSet(viewsets.ModelViewSet):
    queryset = AccountsReceivableTitle.objects.all()
    serializer_class = AccountsReceivableTitleSerializer
    permission_classes = [permissions.IsAdminUser]