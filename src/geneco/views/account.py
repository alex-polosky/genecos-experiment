from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from geneco.models.account import Account
from geneco.serializers.account import AccountSerializer
from geneco.utils import StandardPagination, status_text_to_value, filter_queryset_by_request


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    pagination_class = StandardPagination
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        # TODO: ensure proper permissions for access

        queryset = Account.objects.all().order_by('id')

        filters = {
            'min_balance': 'balance__gte',
            'max_balance': 'balance__lte',
            'consumer_name': 'accountconsumer__consumer__full_name__icontains',
            'status': 'status'
        }
        filter_value_fn = {
            'status': status_text_to_value
        }

        queryset = filter_queryset_by_request(queryset, self.request.query_params, filters, filter_value_fn)

        return queryset

    def get_permissions(self):
        match self.action:
            case 'list', 'retrieve':
                perms = [IsAuthenticated]
            case _:
                perms = [IsAdminUser]
        return [perm() for perm in perms]
