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
