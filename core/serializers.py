from base64 import urlsafe_b64encode
from django.urls import reverse
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_email_verification_token
from django.contrib.auth import get_user_model

User = get_user_model()

# Create a User registration serializer
# When the user sends the request with his data — in this case, email and password —, 
# we create a new user with is_verified=False (builtin field in default user model)
# Then we send an email containing a verification link
# TODO: customize it so the link points to a route in the frontend

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        return data

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        token = generate_email_verification_token.make_token(user)
        verify_path = reverse('verify-email')
        verification_url = f"http://127.0.0.1:8000{verify_path}?uid={user.id}&token={token}"


        # Conteúdo do email
        subject = "Verifique seu email"
        message = (
            "Seja bem vindo!\n\n"
            "Por favor, verifique seu email clicando no link abaixo:\n"
            f"{verification_url}\n\n"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user
