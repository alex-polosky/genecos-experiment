from ._base import BaseModel
from django.db import models


class AccountConsumer(BaseModel):
    account = models.ForeignKey('Account', on_delete=models.DO_NOTHING)
    consumer = models.ForeignKey('Consumer', on_delete=models.DO_NOTHING)
