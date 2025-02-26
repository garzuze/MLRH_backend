import json
from django.shortcuts import get_object_or_404, render
from clients.models import Client, ClientContact
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response

from .serializers import RegistrationSerializer
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from .utils import generate_email_verification_token


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email and password:
            raise self.fail("no_active_acount")
    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise self.fail("no_active_account")

        if not user.check_password(password):
            raise self.fail("no_active_account")

        if not user.is_active:
            raise self.fail("no_active_account")

        data = super().validate(attrs)
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyEmailAPIView(APIView):
    '''
    Receive user's uid and token. If token matches with user, activate the user
    '''
    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        
        if not uid or not token:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=uid)
        
        # If it matches, we can activate the user!
        if generate_email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        for item in data:
            if item["status"] == 0:
                status = False
            else:
                status = True
            contato = ClientContact.objects.create(
                id = item["id"],
                client = Client.objects.get(id=int(item["cliente_id"])),
                name = item["nome"],
                department = item["departamento"],
                phone = item["telefone"],
                email = item["email"],
                status = status,
            )
            contato.save()
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer