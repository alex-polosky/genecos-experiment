from ._base import BaseModel
from django.db import models


class Consumer(BaseModel):
    # TODO: expand full name into first, family, middle, title, etc etc
    full_name = models.CharField(max_length=255)

    # TODO: implement encryption / decryption on-the-fly for this
    ssn = models.CharField(max_length=100)
    ssn_hash = models.CharField(max_length=32, help_text='SHA 256 hash digest of ssn')
