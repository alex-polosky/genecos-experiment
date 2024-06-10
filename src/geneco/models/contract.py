from django.db import models
from geneco.models._base import BaseModel


class Contract(BaseModel):
    agency = models.ForeignKey('Agency', on_delete=models.PROTECT)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)

    # TODO: any contract details?
