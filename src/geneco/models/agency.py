from ._base import BaseModel
from django.db import models


class Agency(BaseModel):
    name = models.CharField(max_length=255)

    # TODO: Contact info
