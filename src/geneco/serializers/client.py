from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.client import Client


class ClientSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    class Meta:
        model = Client
        exclude = ['id']
