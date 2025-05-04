from rest_framework import permissions, viewsets

from finance.models import PayableTitle, ReceivableTitle
from finance.serializers import PayableTitleSerializer, ReceivableTitleSerializer

class ReceivableTitleViewSet(viewsets.ModelViewSet):
    queryset = ReceivableTitle.objects.all()
    serializer_class = ReceivableTitleSerializer
    permission_classes = [permissions.IsAdminUser]


class PayableTitleViewSet(viewsets.ModelViewSet):
    queryset = PayableTitle.objects.all()
    serializer_class = PayableTitleSerializer
    permission_classes = [permissions.IsAdminUser]