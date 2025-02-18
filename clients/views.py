from .models import Client, Benefit, EconomicActivity
from .serializers import ClientSerializer, BenefitSerializer, EconomicActivitySerializer
from rest_framework import permissions, viewsets

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]

