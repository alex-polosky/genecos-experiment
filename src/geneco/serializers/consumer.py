from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.consumer import Consumer
from geneco.serializers.address_lead import AddressLeadSerializer


class ConsumerSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    addresses = AddressLeadSerializer(many=True, read_only=True, source='addresslead_set')

    class Meta:
        model = Consumer
        fields = [
            'uuid',
            'full_name',
            'ssn_hash',
            'addresses'
        ]
