from .models import Client, Benefit, ClientFee, EconomicActivity, ClientContact, Service
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ClientFeeSerializer, ClientSerializer, BenefitSerializer, EconomicActivitySerializer, ClientMinimalSerializer, ClientContactSerializer, ServiceSerializer
from rest_framework import permissions, viewsets

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]


class EconomicActivityViewSet(viewsets.ModelViewSet):
    queryset = EconomicActivity.objects.all()
    serializer_class = EconomicActivitySerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientContactViewSet(viewsets.ModelViewSet):
    queryset = ClientContact.objects.all()
    serializer_class = ClientContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientFeeViewSet(viewsets.ModelViewSet):
    queryset = ClientFee.objects.all()
    serializer_class = ClientFeeSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_clients(request):
    query = request.GET.get("q", "")

    if query:
        clients = Client.objects.filter(corporate_name__icontains=query)[:5]
        serializer = ClientMinimalSerializer(clients, many=True)
        return Response(serializer.data)
    return Response([])