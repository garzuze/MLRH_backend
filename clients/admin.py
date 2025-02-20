from django.contrib import admin

from .models import Client, ClientContact, Benefit, EconomicActivity, Service, ClientFee

class EconomicActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class BenefitAdmin(admin.ModelAdmin):
    list_display = ['id', 'benefit']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'corporate_name', 'cnpj', 'cep', 'number_of_employees', 'economic_activity', 'created_at']
    search_fields = ["cnpj", "corporate_name"]
    list_filter = ["state"]


class ClientContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "client", "department", "phone", "email", "status"]
    search_fields = ["name", "phone"]
    list_filter = ["status"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'type_of_charge', 'deadline']


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientContact, ClientContactAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(EconomicActivity, EconomicActivityAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ClientFee)