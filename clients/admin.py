from django.contrib import admin

from .models import Client, ClientContact, Benefit, EconomicActivity, Service

# Register your models here.

admin.site.register(Client)
admin.site.register(ClientContact)
admin.site.register(Benefit)
admin.site.register(EconomicActivity)
admin.site.register(Service)
