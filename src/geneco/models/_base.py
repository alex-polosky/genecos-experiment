import uuid
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # TODO: decide on implementing soft delete
    # deleted = models.DateTimeField(blank=True, null=True)
