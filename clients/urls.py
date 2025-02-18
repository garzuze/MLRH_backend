from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'benefits', BenefitViewSet, basename='benefit')

urlpatterns = [
    path('', include(router.urls)),
]
