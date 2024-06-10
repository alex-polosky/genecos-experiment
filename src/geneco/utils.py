import base64
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
from rest_framework.pagination import PageNumberPagination

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

class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000
