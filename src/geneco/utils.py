import base64
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
from rest_framework.pagination import PageNumberPagination
from geneco.models.account import AccountStatus

def get_fernet() -> Fernet:
    return Fernet(settings.FERNET_KEY)

def encrypt_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    return get_fernet().encrypt(hex(int(ssn.replace(b'-', b'')))[2:].encode()).decode('utf-8')

def decrypt_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    decrypted = str(int(get_fernet().decrypt(ssn), 16))
    return f'{decrypted[0:3]}-{decrypted[3:5]}-{decrypted[5:]}'

def hash_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    return base64.urlsafe_b64encode(hashlib.sha256(ssn).digest()).decode('utf-8')

def status_text_to_value(text: str) -> int:
    match ' '.join(x for x in text.lower().strip().replace('-', ' ').replace('_', ' ').split(' ') if x):
        case 'inactive':
            return AccountStatus.INACTVE.value
        case 'paid in full':
            return AccountStatus.PAID_IN_FULL.value
        case 'in collection':
            return AccountStatus.IN_COLLECTION.value
        case _:
            return 0

def filter_queryset_by_request(queryset, query_params: dict[str, str], filters: dict[str, str], filter_value_fn: dict[str, any]):
    qs_filters = {}
    for filter_ in filters:
        if (value := query_params.get(filter_, None)):
            search = filters[filter_]
            if filter_ in filter_value_fn:
                value = filter_value_fn[filter_](value)
            qs_filters[search] = value
    if qs_filters:
        queryset = queryset.filter(**qs_filters)
    return queryset

class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000
