from django.db import models
from geneco.models._base import BaseModel


class Client(BaseModel):
    name = models.CharField(max_length=255)

    # TODO: contact info
