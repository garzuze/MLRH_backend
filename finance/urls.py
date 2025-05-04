from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'receivable_title', ReceivableTitleViewSet, basename='receivable_title')
router.register(r'payable_title', PayableTitleViewSet, basename='payable_title')


urlpatterns = router.urls