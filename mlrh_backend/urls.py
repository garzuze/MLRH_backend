from django.contrib import admin
from django.urls import include, path

from clients.views import update_data

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('update_data', update_data),
]
