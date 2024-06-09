from django.contrib import admin
from .models import *


for model in (
    Agency,
    Client,
    Contract,
    Account,
    Consumer,
    AddressLead
):
    admin.site.register(model)

