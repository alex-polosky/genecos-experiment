from ._base import BaseModel
from django.db import models


class Contract(BaseModel):
    agency = models.ForeignKey('Agency', on_delete=models.PROTECT)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    
    # TODO: any contract details?
