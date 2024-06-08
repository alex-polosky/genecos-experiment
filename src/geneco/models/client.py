from ._base import BaseModel
from django.db import models


class Client(BaseModel):
    name = models.CharField(max_length=255)

    # TODO: contact info
