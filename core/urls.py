from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    CustomTokenObtainPairView,
    RegistrationView,
    VerifyEmailAPIView,
    update_data,
    update_languages,
    update_resume,
)

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("update_data/", update_data, name="update_data"),
    path("update_languages/", update_languages, name="update_languages"),
    path("update_resume/", update_resume, name="update_resume"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/register/", RegistrationView.as_view(), name="register"),
    path("api/verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
]
