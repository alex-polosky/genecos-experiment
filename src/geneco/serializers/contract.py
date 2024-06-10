from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.contract import Contract


class ContractSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    class Meta:
        model = Contract
        exclude = ['id']
