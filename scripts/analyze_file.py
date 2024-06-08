import csv
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'consumers_balances.csv')
OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'consumers_balances.group.json')


def main():
    with open(PATH) as f:
        c = csv.DictReader(f)
        rows = [r for r in c]

    headers = rows[0].keys()
    data = {
        k: {}
        for k in headers
    }

    for row in rows:
        for header in headers:
            if header == 'balance':
                continue
            value = row[header]
            if not value in data[header]:
                data[header][value] = []
            data[header][value].append(row)

    with open(OUT, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    main()
