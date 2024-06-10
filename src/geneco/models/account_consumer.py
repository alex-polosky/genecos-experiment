from django.db import models
from geneco.models._base import BaseModel


class AccountConsumer(BaseModel):
    account = models.ForeignKey('Account', on_delete=models.DO_NOTHING)
    consumer = models.ForeignKey('Consumer', on_delete=models.DO_NOTHING)
