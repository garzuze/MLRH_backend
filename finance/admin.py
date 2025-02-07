from django.contrib import admin

from .models import AccountsReceivableTitle, AccountsPayableTitle

admin.site.register(AccountsReceivableTitle)
admin.site.register(AccountsPayableTitle)