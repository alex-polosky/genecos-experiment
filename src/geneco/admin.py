from django.contrib import admin
from .models import *


for model in (
    Agency,
    Client,
    Contract,
    # Account,
    Consumer,
    AddressLead
):
    admin.site.register(model)


class ConsumerInline(admin.TabularInline):
    model = Account.consumers.through


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (ConsumerInline,)
