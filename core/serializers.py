from base64 import urlsafe_b64encode
import os
from smtplib import SMTPException
from django.http import BadHeaderError
from django.urls import reverse
from rest_framework.exceptions import ValidationError, ParseError

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
        fields = ('email', 'password', 'cpf', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = generate_email_verification_token.make_token(user)
        verification_url = f"{os.environ.get('FRONTEND_URL')}/verify-email?uid={user.id}&token={token}"

        subject = "Verifique seu email"
        plain_message = (
            "Seja bem vindo!\n\n"
            "Por favor, verifique seu email clicando no link abaixo:\n"
            f"{verification_url}\n\n"
        )
        
        html_message = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333333;
            }}
            p {{
                color: #555555;
                line-height: 1.5;
            }}
            .button {{
                display: inline-block;
                background-color: #28a745;
                color: #ffffff;
                padding: 10px 20px;
                margin: 20px 0;
                text-decoration: none;
                border-radius: 5px;
            }}
            .footer {{
                font-size: 12px;
                color: #999999;
                text-align: center;
                margin-top: 20px;
            }}
            </style>
        </head>
        <body>
            <div class="container">
            <h1>Bem Vindo!</h1>
            <p>Obrigado por se registrar. Por favor, verifique seu email clicando no botão abaixo:</p>
            <p style="text-align: center;">
                <a href="{verification_url}" class="button">Verificar Email</a>
            </p>
            <p>Se você não criou essa conta, por favor, ignore este email.</p>
            </div>
            <div class="footer">
            &copy; 2025 MLRH. Todos os direitos reservados.
            </div>
        </body>
        </html>
        """

        # http://stackoverflow.com/questions/41457565/how-to-catch-email-sending-exceptions-in-django-1-10
        try:
            send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        except BadHeaderError:              # If mail's Subject is not properly formatted.
            print('Invalid header found.')
            user.delete()
            raise ValidationError
        except SMTPException as e:          # It will catch other errors related to SMTP.
            user.delete()
            print('There was an error sending an email.'+ e)
            raise ValidationError
        except:                             # It will catch All other possible errors.
            user.delete()
            print("Mail Sending Failed!")
            raise ValidationError

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'cpf']

