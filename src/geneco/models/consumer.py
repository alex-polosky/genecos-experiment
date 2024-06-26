from django.db import models
from geneco.models._base import BaseModel


class Consumer(BaseModel):
    # TODO: expand full name into first, family, middle, title, etc etc
    full_name = models.CharField(max_length=255)

    # TODO: implement encryption / decryption on-the-fly for this
    ssn = models.CharField(max_length=100)
    ssn_hash = models.CharField(max_length=64, help_text='base64 repr of SHA 256 hash digest of ssn')

    # TODO: possible extra data (ie: aliases, phones, emails)
