import json
from django.shortcuts import render
from clients.models import Service
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        for item in data:
            service = Service(
                id = item["id"],
                service = item["descricao"],
                type_of_charge = item["tipoCobranca"],
                deadline = item["prazo"],
            )
            service.save()
            
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')