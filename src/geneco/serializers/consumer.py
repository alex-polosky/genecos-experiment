from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.consumer import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    class Meta:
        model = Consumer
        exclude = ['id']
