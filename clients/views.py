from .models import Client, Benefit, EconomicActivity
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ClientSerializer, BenefitSerializer, EconomicActivitySerializer, ClientMinimalSerializer
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_clients(request):
    query = request.GET.get("q", "")

    if query:
        clients = Client.objects.filter(corporate_name__icontains=query)[:5]
        serializer = ClientMinimalSerializer(clients, many=True)
        return Response(serializer.data)
    return Response([])