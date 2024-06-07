from ._base import BaseModel
from django.db import models


class Account(BaseModel):
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)
