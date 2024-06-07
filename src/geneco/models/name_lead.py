from ._base import BaseModel
from django.db import models


class NameLead(BaseModel):
    consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)
