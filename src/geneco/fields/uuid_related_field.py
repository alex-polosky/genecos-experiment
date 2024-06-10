from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import RelatedField, HyperlinkedRelatedField
from logging import getLogger
log = getLogger(__file__)


class UUIDRelatedField(RelatedField):
    lookup_field = 'uuid'

    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid uuid "{uuid}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected UUID value, received {data_type}.'),
    }

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.lookup_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', uuid=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return getattr(value, self.lookup_field)
