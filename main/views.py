from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

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
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
