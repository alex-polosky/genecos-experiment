from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from geneco.models.address_lead import AddressLead
from geneco.serializers.address_lead import AddressLeadSerializer
from geneco.utils import StandardPagination


class AddressLeadViewSet(viewsets.ModelViewSet):

    serializer_class = AddressLeadSerializer
    pagination_class = StandardPagination
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        # TODO: ensure proper permissions for access
        return AddressLead.objects.all().order_by('id')

    def get_permissions(self):
        match self.action:
            case 'list', 'retrieve':
                perms = [IsAuthenticated]
            case _:
                perms = [IsAdminUser]
        return [perm() for perm in perms]
