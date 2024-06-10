import csv
import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import F, TextField
from django.db.models.functions import Concat
from django.db.transaction import atomic
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status as rest_status
from geneco.models import Account, AccountConsumer, AccountStatus, AddressLead, Consumer, Contract
from geneco.utils import encrypt_ssn, hash_ssn


@api_view(['PUT'])
@parser_classes([MultiPartParser])
def AccountIngestView(request: Request, contract: UUID) -> Response:
    try:
        contract_obj = Contract.objects.get(uuid=contract)
    except Contract.DoesNotExist:
        pass

    file_obj: InMemoryUploadedFile = request.data.get('file')
    rows = csv.reader((x.decode('utf-8') for x in file_obj.readlines()))
    results = ingest_contents(contract_obj, rows)

    return Response(status=rest_status.HTTP_201_CREATED, data=results)

def ingest_contents(contract: Contract, rows: list) -> dict[str, list[str | tuple[list[str], list[str]]]]:
    accounts, consumers, addresses, acc_cons, errors = parse_contents(contract, rows)

    filter_existing_consumers(consumers)
    filter_existing_addresses(addresses)

    with atomic():
        try:
            account_ids = [str(x.uuid) for x in Account.objects.bulk_create(accounts.values())]
            consumer_ids = [str(x.uuid) for x in Consumer.objects.bulk_create(consumers.values())]
            address_ids = [str(x.uuid) for x in AddressLead.objects.bulk_create(addresses.values())]
            acc_con_ids = [str(x.uuid) for x in AccountConsumer.objects.bulk_create(acc_cons.values())]
        except Exception as ex:
            account_ids = consumer_ids = address_ids = acc_con_ids = []
            errors.append((['server'], ['500']))
            raise

    return {
        'accounts': account_ids,
        'consumers': consumer_ids,
        'addresses': address_ids,
        'account_consumers': acc_con_ids,
        'errors': errors
    }

def parse_contents(contract: Contract, rows: list[list[str]]) -> tuple[dict[str, Account], dict[str, Consumer], dict[str, AddressLead], dict[UUID, AccountConsumer], list[str | tuple[list[str], list[str]]]]:
    errors: list[str | tuple[list[str], list[str]]] = []
    accounts: dict[str, Account] = {}  # client ref no
    consumers: dict[str, Consumer] = {}  # ssn
    addresses: dict[str, AddressLead] = {} # address.unique()
    acc_cons: dict[UUID, AccountConsumer] = {} # uuid

    # Assume header
    used_header = False
    for row in rows:
        if not used_header:
            used_header = True
            continue

        client_ref, balance, status, name, address, ssn = row

        row_errors = []

        try:
            balance = Decimal(balance)
        except:
            row_errors.append('balance')
        if status.lower() == 'inactive':
            status_code = AccountStatus.INACTVE.value
        elif status.lower().replace('_', ' ').replace('-', '') == 'paid in full':
            status_code = AccountStatus.PAID_IN_FULL.value
        elif status.lower().replace('_', ' ').replace('-', ' ') == 'in collection':
            status_code = AccountStatus.IN_COLLECTION.value
        else:
            row_errors.append('status')
        add_lines = address.split('\n')
        if len(add_lines) == 1:
            line1 = address
            line2 = ''
        elif len(add_lines) == 2:
            line1, line2 = add_lines
        else:
            row_errors.append('address')

        ssn_enced = encrypt_ssn(ssn)
        ssn_hashed = hash_ssn(ssn)

        if row_errors:
            del row[-1]
            errors.append((row, row_errors))
            continue

        if client_ref in accounts:
            account = accounts[client_ref]
        else:
            # process balance / status only once; check README for why
            account = Account(
                uuid = uuid4(),
                contract=contract,
                client_reference=client_ref,
                status=status_code,
                debt=balance,
                balance=balance
            )
            accounts[client_ref] = account

        if ssn_hashed in consumers:
            consumer = consumers[ssn_hashed]
        else:
            consumer = Consumer(
                uuid = uuid4(),
                full_name=name,
                ssn=ssn_enced,
                ssn_hash=ssn_hashed
            )
            consumers[ssn_hashed] = consumer

        lead = AddressLead(
            uuid=uuid4(),
            consumer=consumer,
            line1=line1,
            line2=line2,
            reported=datetime.datetime.now(datetime.UTC)
        )
        if not (lead_hash := lead.unique()) in addresses:
            addresses[lead_hash] = lead

        acid = uuid4()
        acc_cons[acid] = AccountConsumer(uuid=acid, account=account, consumer=consumer)

    return (
        accounts,
        consumers,
        addresses,
        acc_cons,
        errors
    )

def filter_existing_consumers(consumers: dict[str, Consumer]) -> None:
    exist_consumers = Consumer.objects.filter(ssn_hash__in=consumers.keys())
    for consumer in exist_consumers:
        this_consumer = consumers[consumer.ssn_hash]
        this_consumer.id = consumer.id
        this_consumer.refresh_from_db()
        del consumers[consumer.ssn_hash]

def filter_existing_addresses(addresses: dict[str, AddressLead]) -> None:
    # When the consumers get refreshed from the db, their uuid are updated,
    # and the uuid is part of what makes the unique address,
    # so we need access to both the crafted and db uuid
    new_uniques = {v.unique(): (old_key ,v) for (old_key, v) in addresses.items()}
    exist_addresses = AddressLead.objects.annotate(
        adds=Concat(F('consumer__uuid'), F('line1'), F('line2'), output_field=TextField())
    ).filter(adds__in=new_uniques.keys())
    for address in exist_addresses:
        this_address = new_uniques[address.unique()][1]
        this_address.id = address.id
        this_address.refresh_from_db()
        del addresses[new_uniques[address.unique()][0]]
