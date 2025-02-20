from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'benefits', BenefitViewSet, basename='benefit')
router.register(r'economic_activity', EconomicActivityViewSet, basename='economic_activity')
router.register(r'client_contact', ClientContactViewSet, basename="client_contact")
router.register(r'services', ServiceViewSet, basename="services")
router.register(r'client_fee', ClientFeeViewSet, basename="client_fee")


urlpatterns = [
    path("search_clients/", search_clients, name="search_clients")
]

urlpatterns += router.urls