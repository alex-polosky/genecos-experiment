import pytest
from test.utils import *

@pytest.fixture
def db_setup_initial(db):
    from geneco.models import Agency, Client, Contract
    gen_id_save(Agency(id=1, name='GeneCo Repo Men'))
    gen_id_save(Client(id=1, name='GeneCo Organ Emporium'))
    gen_id_save(Contract(id=1, agency_id=1, client_id=1))

@pytest.fixture
def ssn_direct(monkeypatch):
    def mock_encrypt_ssn(ssn):
        return ssn
    def mock_hash_ssn(ssn):
        return ssn
    import geneco.utils
    monkeypatch.setattr(geneco.utils, 'encrypt_ssn', mock_encrypt_ssn)
    monkeypatch.setattr(geneco.utils, 'hash_ssn', mock_hash_ssn)
