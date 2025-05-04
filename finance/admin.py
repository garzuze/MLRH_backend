from django.contrib import admin

from .models import ReceivableTitle, PayableTitle

admin.site.register(ReceivableTitle)
admin.site.register(PayableTitle)