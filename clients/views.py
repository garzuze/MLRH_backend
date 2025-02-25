from .models import Client, Benefit, ClientFee, EconomicActivity, ClientContact, Service
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ClientFeeSerializer, ClientSerializer, BenefitSerializer, EconomicActivitySerializer, ClientMinimalSerializer, ClientContactSerializer, ServiceSerializer
from rest_framework import permissions, viewsets, status

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]


class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAdminUser]


class EconomicActivityViewSet(viewsets.ModelViewSet):
    queryset = EconomicActivity.objects.all()
    serializer_class = EconomicActivitySerializer
    permission_classes = [permissions.IsAdminUser]


class ClientContactViewSet(viewsets.ModelViewSet):
    queryset = ClientContact.objects.all()
    serializer_class = ClientContactSerializer
    permission_classes = [permissions.IsAdminUser]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]


class ClientFeeViewSet(viewsets.ModelViewSet):
    queryset = ClientFee.objects.all()
    serializer_class = ClientFeeSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        client = request.data.get('client')
        service = request.data.get('service')

        if client and service:
            existing_fee = ClientFee.objects.filter(client=client, service=service).first()

            if existing_fee:
                serializer = self.get_serializer(existing_fee, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return super().create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def search_clients(request):
    query = request.GET.get("q", "")

    if query:
        clients = Client.objects.filter(corporate_name__icontains=query)[:5]
        print(clients)
        serializer = ClientMinimalSerializer(clients, many=True)
        return Response(serializer.data)
    return Response([])


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_client_contacts(request):
    query = request.GET.get("q", "")

    if query:
        contacts = ClientContact.objects.filter(client__id=query)
        serializer = ClientContactSerializer(contacts, many=True)
        return Response(serializer.data)
    return Response([])


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_client_fees(request):
    query = request.GET.get("q", "")

    if query:
        client_fees = ClientFee.objects.filter(client__id=query)
        serializer = ClientFeeSerializer(client_fees, many=True)
        return Response(serializer.data)
    return Response([])