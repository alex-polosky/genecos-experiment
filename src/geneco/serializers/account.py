from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.account import Account
from geneco.models.consumer import Consumer
from geneco.serializers.consumer import ConsumerSerializer
from geneco.serializers.account_consumer import AccountConsumerSerializer


class AccountSerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField

    consumers = serializers.SerializerMethodField()

    def get_consumers(self, obj: Account) -> str:
        query = Consumer.objects.filter(id__in=obj.accountconsumer_set.all().values_list('consumer_id', flat=True))
        return ConsumerSerializer(query, read_only=True, many=True, source='accountconsumer_set__consumer').data

    class Meta:
        model = Account
        fields = [
            'uuid',
            'created',
            'updated',
            'client_reference',
            'debt',
            'balance',
            'status',
            'contract',
            'consumers'
        ]
