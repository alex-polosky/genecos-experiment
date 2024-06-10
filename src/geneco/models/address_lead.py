from ._base import BaseModel
from django.db import models


class AddressLead(BaseModel):
    consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)

    reported = models.DateTimeField()  # The datetime that the consumer was reported to be here; often just the ingested dt
    line1 = models.TextField()
    line2 = models.TextField()

    def unique(self):
        return str(self.consumer.uuid) + self.line1 + self.line2
