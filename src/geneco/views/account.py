from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from geneco.models.account import Account
from geneco.serializers.account import AccountSerializer
from geneco.utils import StandardPagination


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    pagination_class = StandardPagination
    lookup_field = 'uuid'
    # lookup_value_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        # TODO: ensure proper permissions for access
        return Account.objects.all().order_by('id')

    def get_permissions(self):
        match self.action:
            case 'list', 'retrieve':
                perms = [IsAuthenticated]
            case _:
                perms = [IsAdminUser]
        return [perm() for perm in perms]