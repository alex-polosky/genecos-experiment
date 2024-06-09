'''For use in vscode / native with debugging!'''

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(
    BASE_DIR,
    'src'
))

with open(os.path.join(BASE_DIR, '.env')) as f:
    for line in f.readlines():
        if not line or line.startswith('#') or not '=' in line:
            continue
        os.environ.setdefault(*line.split('=', 1))

os.environ['DB_HOST_IP'] = 'localhost'
os.environ['DB_HOST_PORT'] = '5499'

django.setup()

###############################

import base64
import csv
import datetime
from geneco.models import *
from geneco.utils import *
from geneco.views.account_ingest import ingest_contents

contract = Contract.objects.first()
with open(os.path.join(BASE_DIR, 'data', 'consumers_balances.csv'), 'rb') as f:
    rows = csv.reader((x.decode('utf-8') for x in f.readlines()))

# AccountConsumer.objects.all().delete(); Account.objects.all().delete(); AddressLead.objects.all().delete(); Consumer.objects.all().delete()

try:
    Consumer(
        pubk='00000000-0000-0000-0010-000000000001',
        full_name='Christopher Harrison',
        ssn='gAAAAABmZQ6pup7xvoFaX-_O52ZhAAiLOsNvFEJ9cntIxDjRRD7SRjbvWwVWuPQxJXycGKOfSSyUtM3QgXDUdfR_UhFFeLSjtg==',
        ssn_hash=base64.urlsafe_b64encode(b'\xf6r,\xf1\x0f\xf1u\xc7\x9eq\x10Nq\xb1\xf6\xa4D\x92C\xd4}\x95\xd3I1\xa0A\xdaEB\xe7\xbc').decode('utf-8'),
    ).save()
    con = Consumer(
        pubk='00000000-0000-0000-0010-000000000002',
        full_name='Heather Nelson',
        ssn='gAAAAABmZQ70nfWHGx4WCL0bDH2fTMA0NwcuURgVn2HoHlCQPmXlwh19R_So71IiJpk9eqnb8NF9Bp6cEY8PgtJwxiza8KheKg==',
        ssn_hash=base64.urlsafe_b64encode(b'B\xbd&\xbe\x89\x06)m\xf6\xf0\xf9&\xa2\xdf\xacWb$\xd8\xb42J\xae\xa5x\xfe\xc0t&\x19&\x9e').decode('utf-8'),
    )
    con.save()
    AddressLead(
        pubk='00000000-0000-0000-0020-000000000001',
        consumer=con,
        reported=datetime.datetime.now(datetime.UTC),
        line1='3719 Daniel Point Apt. 234',
        line2='Lake Jaredborough, SD 04725'
    ).save()
except BaseException as ex:
    print(ex)

ingest_contents(contract, rows)
