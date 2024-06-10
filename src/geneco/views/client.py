from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from geneco.models.client import Client
from geneco.serializers.client import ClientSerializer
from geneco.utils import StandardPagination


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    pagination_class = StandardPagination
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        # TODO: ensure proper permissions for access
        return Client.objects.all().order_by('id')

    def get_permissions(self):
        match self.action:
            case 'list', 'retrieve':
                perms = [IsAuthenticated]
            case _:
                perms = [IsAdminUser]
        return [perm() for perm in perms]
