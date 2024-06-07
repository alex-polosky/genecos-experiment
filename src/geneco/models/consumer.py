from ._base import BaseModel
from django.db import models


class Consumer(BaseModel):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    verified_name = models.OneToOneField('NameLead', null=True, related_name='verified', on_delete=models.SET_NULL)
    verified_address = models.OneToOneField('AddressLead', null=True, related_name='verified', on_delete=models.SET_NULL)
    verified_ssn = models.OneToOneField('SSNLead', null=True, related_name='verified', on_delete=models.SET_NULL)
