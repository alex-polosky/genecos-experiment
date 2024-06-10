from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from geneco.models.account import Account
from geneco.serializers.account import AccountSerializer
from geneco.utils import StandardPagination


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    pagination_class = StandardPagination
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        # TODO: ensure proper permissions for access

        username = self.request.query_params.get('username')
        # filters = {
        #     'client_reference': '',
        #     'debt'
        # }

        return Account.objects.all().order_by('id')

    def get_permissions(self):
        match self.action:
            case 'list', 'retrieve':
                perms = [IsAuthenticated]
            case _:
                perms = [IsAdminUser]
        return [perm() for perm in perms]
