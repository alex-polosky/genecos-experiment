from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.account_consumer import AccountConsumer


class AccountConsumerSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    class Meta:
        model = AccountConsumer
        exclude = ['id']
