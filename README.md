# GeneCo's Collections Software Experiment

"fun blurb here"

## Setup

`git clone [insert link here] && cd [name of repo]`

`docker compose build`

`docker compose up -d`

`docker compose exec -it col_api python manage.py migrate`

`docker compose exec -it col_api python manage.py createsuperuser`

Open [the server page](http://localhost:8999/admin/) to view the admin dash!

## Relation setup

There are multiple entities (TODO: usertypes?):
- Agency
- Client
- Consumer

`Agency`s contract work out to `Client`s, via a `Contract`

Every `Account` is opened from a `Contract`

Every `Account` can have multiple `Consumer`s through `AccountConsumer`

Every `Consumer` can have multiple `AddressLead`s (TODO: add email, phone, etc)

## Sensitive data

Need to find a way to sensitively store SSN and other PII

Add hashing for lookups

Best bet is to encrypt with a key loaded in the env; perfect would be creating a custom field

Found a few packages that -might- work, but everything's woefully out of date
 - https://github.com/chrisclark/django-cryptography

---

We're going to store the SSNs encrypted by:
`Fernet(key).encrypt(hex(int(ssn.replace('-', '')))[2:].encode())`

Decrypt:
`int(Fernet(key).decrypt(ssn), 16)` followed by some string manipulation to get the hyphons back

## Branches

Currently there are four branches:
- main
    - This is the current best version of the code
- django
    - Django only version
- drf
    - Api built with [django-rest-framework](https://www.django-rest-framework.org/)
- ninja
    - Api built with [django-ninja](https://django-ninja.dev/), which is a newer framework I came across that looks easier to spin up than drf, so I want to check it out ([also similar to something I built for Clubcard back in the day](https://github.com/alex-polosky/django-api-framework))

drf / ninja won't be looked at until I get a different front end put on

## To-dos!

- debate on auto-migrations
    - on one hand, ease of programming
    - on other hand, could break db if not ready?
    - on original hand, that's the whole point of migrations and test scripts??
- implement ssn decryption
- implement on the fly encrypt / decrypt for ssn
- expand consumer name information
- add per-consumer debt collected information on accountconsumer
- logging actions on accounts / consumers
- expand address information
    - currently there's formats that I haven't even seen (ships in the middle of Iowa?)
    - perfected address parsing is a -hard- problem anyways and should be solved by a 3rd party solution, unless that's what we're solving
