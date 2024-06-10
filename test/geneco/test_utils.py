from contextlib import nullcontext as does_not_raise
import pytest

def test_get_fernet():
    from cryptography.fernet import Fernet
    from geneco.utils import get_fernet
    with does_not_raise():
        fernet = get_fernet()
    assert type(fernet) == Fernet

def test_encrypt_ssn_no_error():
    from geneco.utils import encrypt_ssn
    with does_not_raise():
        enc = encrypt_ssn('000-00-0000')

def test_encrypt_ssn_is_str():
    from geneco.utils import encrypt_ssn
    enc = encrypt_ssn('000-00-0000')
    assert type(enc) == str

def test_encrypt_ssn_length():
    from geneco.utils import encrypt_ssn
    enc = encrypt_ssn('000-00-0000')
    assert len(enc) == 100

def test_encrypt_ssn_urlsafe_b64():
    from base64 import urlsafe_b64decode
    from geneco.utils import encrypt_ssn
    enc = encrypt_ssn('000-00-0000')
    with does_not_raise():
        urlsafe_b64decode(enc)

def test_encrypt_decrypt_ssn_no_error():
    from geneco.utils import encrypt_ssn, decrypt_ssn
    ssn = '999-99-9999'
    enc = encrypt_ssn(ssn)
    with does_not_raise():
        dec = decrypt_ssn(enc)

def test_encrypt_decrypt_ssn_equals():
    from geneco.utils import encrypt_ssn, decrypt_ssn
    ssn = '999-99-9999'
    enc = encrypt_ssn(ssn)
    dec = decrypt_ssn(enc)
    assert ssn == dec

def test_encrypt_decrypt_ssn_is_str():
    from geneco.utils import encrypt_ssn, decrypt_ssn
    ssn = '999-99-9999'
    enc = encrypt_ssn(ssn)
    dec = decrypt_ssn(enc)
    assert type(dec) == str

def test_hash_ssn_no_error():
    from geneco.utils import hash_ssn
    ssn = '999-99-9999'
    with does_not_raise():
        h = hash_ssn(ssn)

def test_hash_ssn_is_str():
    from geneco.utils import hash_ssn
    ssn = '999-99-9999'
    h = hash_ssn(ssn)
    assert type(h) == str

def test_hash_ssn_length():
    from geneco.utils import hash_ssn
    ssn = '999-99-9999'
    h = hash_ssn(ssn)
    assert len(h) == 44

def test_hash_ssn_urlsafe_b64():
    from base64 import urlsafe_b64decode
    from geneco.utils import hash_ssn
    ssn = '999-99-9999'
    h = hash_ssn(ssn)
    with does_not_raise(h):
        urlsafe_b64decode(h)

@pytest.mark.parametrize('input,expected',[
    ('inactive', 1),
    ('INACTIVE', 1),
    ('     iNaC tIvE     ', 0),
    ('paid in full', 2),
    ('paid in             full            ', 2),
    ('PAID IN FULL', 2),
    ('in collection', 4),
    ('in CollEction', 4),
    ('oivujwerj', 0),
])
def test_status_text_to_value(input, expected):
    from geneco.utils import status_text_to_value
    assert status_text_to_value(input) == expected

# TODO!
def test_filter_queryset_by_request():
    pass
