import pytest
from test.fixtures import db_setup_initial, ssn_direct
from test.utils import gen_id_save, normalize_for_compare

def test_ingest_contents():
    # TODO: decide on testing this;
    # this is really just calling the rest of the functions and then ingesting them
    pass

@pytest.mark.usefixtures('db_setup_initial', 'ssn_direct')
def test_parse_contents():
    # TODO: add error unit tests

    from decimal import Decimal
    import datetime
    from uuid import uuid4
    from geneco.models import Contract, Account, AccountStatus, Consumer, AddressLead, AccountConsumer

    reported = datetime.datetime.now(datetime.UTC)
    contract = Contract.objects.first()

    incoming = [
        x.split(',')
        for x in (
        'assume-header-so-ignore-this',
        '0,123.45,inactive,josh,that one place,1',
        '1,13.45,paid in full,jane,that one place\ndown the road,2',
        '2,5443.45,in collection,blarn,ya know,3',
        '2,5443.45,in collection,josh,ya know,1',
        '3,54.45,in collection,josh,ya know,1',
    )]

    accounts = [
        Account(id=10, uuid=uuid4(), contract=contract, client_reference='0', debt=Decimal('123.45'), balance=Decimal('123.45'), status=AccountStatus.INACTVE.value),
        Account(id=11, uuid=uuid4(), contract=contract, client_reference='1', debt=Decimal('13.45'), balance=Decimal('13.45'), status=AccountStatus.PAID_IN_FULL.value),
        Account(id=12, uuid=uuid4(), contract=contract, client_reference='2', debt=Decimal('5443.45'), balance=Decimal('5443.45'), status=AccountStatus.IN_COLLECTION.value),
        Account(id=13, uuid=uuid4(), contract=contract, client_reference='3', debt=Decimal('54.45'), balance=Decimal('54.45'), status=AccountStatus.IN_COLLECTION.value),
    ]
    consumers = [
        Consumer(id=10, uuid=uuid4(), full_name='josh', ssn='1', ssn_hash='1'),
        Consumer(id=11, uuid=uuid4(), full_name='jane', ssn='2', ssn_hash='2'),
        Consumer(id=12, uuid=uuid4(), full_name='blarn', ssn='3', ssn_hash='3'),
    ]
    leads = [
        AddressLead(id=10, uuid=uuid4(), consumer=consumers[0], reported=reported, line1='that one place', line2=''),
        AddressLead(id=11, uuid=uuid4(), consumer=consumers[1], reported=reported, line1='that one place', line2='down the road'),
        AddressLead(id=12, uuid=uuid4(), consumer=consumers[2], reported=reported, line1='ya know', line2=''),
        AddressLead(id=13, uuid=uuid4(), consumer=consumers[0], reported=reported, line1='ya know', line2=''),
    ]
    acc_cons = [
        AccountConsumer(id=10, uuid=uuid4(), account=accounts[0], consumer=consumers[0]),
        AccountConsumer(id=12, uuid=uuid4(), account=accounts[1], consumer=consumers[1]),
        AccountConsumer(id=10, uuid=uuid4(), account=accounts[2], consumer=consumers[2]),
        AccountConsumer(id=10, uuid=uuid4(), account=accounts[2], consumer=consumers[0]),
        AccountConsumer(id=10, uuid=uuid4(), account=accounts[3], consumer=consumers[0]),
    ]

    expected = [
        accounts,
        consumers,
        leads,
        acc_cons,
        []
    ]

    from geneco.views.account_ingest import parse_contents
    actual = [x.values() if type(x) == dict else x for x in parse_contents(contract, incoming)]

    normalize = lambda obj: [[normalize_for_compare(y) for y in x] for x in obj]
    assert normalize(expected) == normalize(actual)

@pytest.mark.usefixtures('db_setup_initial', 'ssn_direct')
def test_filter_existing_consumers():
    from uuid import uuid4
    from geneco.models import Consumer

    exist_consumers = [
        gen_id_save(Consumer(full_name='John Doe', ssn='1', ssn_hash='1')),
        gen_id_save(Consumer(full_name='Jane Doe', ssn='2', ssn_hash='2')),
        gen_id_save(Consumer(full_name='John Smith', ssn='3', ssn_hash='3'))
    ]
    for x in exist_consumers:
        x.id = None

    new_consumers = [
        Consumer(uuid=uuid4(), full_name='Abe Cool', ssn='10', ssn_hash='10'),
        Consumer(uuid=uuid4(), full_name='Bob Cool', ssn='11', ssn_hash='11'),
        Consumer(uuid=uuid4(), full_name='Cat Cool', ssn='12', ssn_hash='12'),
        Consumer(uuid=uuid4(), full_name='Dog Cool', ssn='13', ssn_hash='13'),
    ]

    incoming = {
        x.ssn_hash: x
        for x in exist_consumers + new_consumers
    }

    from geneco.views.account_ingest import filter_existing_consumers
    filter_existing_consumers(incoming)

    assert [x.ssn_hash for x in incoming.values()] == [x.ssn_hash for x in new_consumers]

@pytest.mark.usefixtures('db_setup_initial', 'ssn_direct')
def test_filter_existing_addresses():
    import datetime
    from uuid import uuid4
    from geneco.models import Consumer, AddressLead

    reported = datetime.datetime.now(datetime.UTC)

    con = gen_id_save(Consumer(full_name='John Doe', ssn='1', ssn_hash='1'))

    exist_leads = [
        gen_id_save(AddressLead(consumer=con, reported=reported, line1='this is line1')),
        gen_id_save(AddressLead(consumer=con, reported=reported, line1='this is line1', line2='line2')),
    ]

    new_leads = [
        AddressLead(uuid=uuid4(), consumer=con, reported=reported, line1='new line1'),
        AddressLead(uuid=uuid4(), consumer=Consumer(uuid=uuid4(), full_name='Abe Cool', ssn='10', ssn_hash='10'), reported=reported, line1='new line1'),
        AddressLead(uuid=uuid4(), consumer=Consumer(uuid=uuid4(), full_name='Bob Cool', ssn='11', ssn_hash='11'), reported=reported, line1='next'),
    ]

    incoming = {
        x.unique(): x
        for x in exist_leads + new_leads
    }

    from geneco.views.account_ingest import filter_existing_addresses
    filter_existing_addresses(incoming)

    assert [x.unique() for x in incoming.values()] == [x.unique() for x in new_leads]
