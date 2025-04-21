from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'receivable_title', AccountsReceivableTitleViewSet, basename='receivable_title')

urlpatterns = router.urls