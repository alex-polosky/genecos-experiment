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

Every `Account` is opened from a `Contract`, and is attached to a `Consumer`

Every `Consumer` has possible `NameLead`s, `AddressLead`s, and `SSNLeads` (TODO: add support for email, phone, etc), and if one data is verified to be the exact match, it can be set on the `Consumer`

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
