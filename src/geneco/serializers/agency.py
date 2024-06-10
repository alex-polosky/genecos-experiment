from rest_framework import serializers
from geneco.fields.uuid_related_field import UUIDRelatedField
from geneco.models.agency import Agency


class AgencySerializer(serializers.ModelSerializer):
    serializer_related_field = UUIDRelatedField
    class Meta:
        model = Agency
        exclude = ['id']
