from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('clients/', include('clients.urls')),
    path('hr/', include('hr.urls')),
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]
