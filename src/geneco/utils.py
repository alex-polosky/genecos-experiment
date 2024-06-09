import base64
from cryptography.fernet import Fernet
import hashlib
from django.conf import settings

def get_fernet() -> Fernet:
    return Fernet(settings.FERNET_KEY)

def encrypt_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    return get_fernet().encrypt(hex(int(ssn.replace(b'-', b'')))[2:].encode()).decode('utf-8')

def decrypt_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    return '{s[0:3]}-{s[3:5]}-{s[5:]}'.format(
        str(int(get_fernet().decrypt(ssn), 16))
    )

def hash_ssn(ssn: str | bytes) -> str:
    if type(ssn) == str:
        ssn = ssn.encode()
    return base64.urlsafe_b64encode(hashlib.sha256(ssn).digest()).decode('utf-8')
