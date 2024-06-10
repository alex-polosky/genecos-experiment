# GeneCo's Collections Software Experiment

"fun blurb here"

## Setup

`git clone [insert link here] && cd [name of repo]`

`docker compose build`

`docker compose up -d`

`docker compose exec -it col_api python manage.py migrate`

`docker compose exec -it col_api python manage.py createsuperuser`

`docker compose exec -it col_api python manage.py loaddata initial-data`

## Running commands

### Admin console

Open [the server page](http://localhost:8999/admin/) to view the admin dash!

### Loading consumers balances test data

`cp /path/to/consumers_balances.csv ./data/consumers_balances.csv`

`curl -X post http://localhost:8999/api/v1/token/ -d "username=insert_user_from_above&password=insert_pw_from_above"`

Note the token value

`curl -X put -H "Authorization: Token $TOKEN" http://localhost:8999/api/v1/contract/00000000-0000-0000-0003-000000000001/ingest/ --form 'file=@"data/consumers_balances.csv"'`

### Running test suite

`docker compose --profile test up -d && docker compose logs --since 0s -f col_api_test`

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

## To-dos!

### key
- ! : implement before a "go live"
- ? : discussion needed

---

- debate on auto-migrations
    - on one hand, ease of programming
    - on other hand, could break db if not ready?
    - on original hand, that's the whole point of migrations and test scripts??
- ! implement on the fly encrypt / decrypt for ssn
- expand consumer name information
- ! add per-consumer debt collected information on accountconsumer
- expand address information
    - currently there's formats that I haven't even seen (ships in the middle of Iowa?)
    - perfected address parsing is a -hard- problem anyways and should be solved by a 3rd party solution, unless that's what we're solving
- ! encrypt local env file for sensitive values using git-crypt
- extra data on consumers
    - name aliases
    - emails
    - phones
- ? make the ingest endpoint not dependent on a named parameter
- ? add parameter to ingest endpoint to determine if headers are involved
- ? add parameter to ingest endpoint for custom headers / placements / mapping
- ? ingest endpoint: add fuzzy matching for status code
- ingest endpoint: add some processing to account debt value
    - I noticed that each non-unique debt still lists the value, but from a cursorary glance they're all the same
- ! add ingest endpoint log mechanism
    - allows for an UI to be made for users to view file processing
    - add location uri for ingested file
    - add async processing
- ? make ssn hash field unique?
    - gut instinct is that this makes sense, and we can associate consumer data and make that hash lookup faster
- fancy json api error pages for api
- openapi schema generation
- better admin console for models
- better __repr__ strings for models
- !! implement tests for ingestion and utils!
- !! ensure that a contract exists for the ingestion !!
- ! different user types for use with the token, and actual permissions
    - IE only agencies should be able to drop new ingest files into the api
- ! expand account ingest tests
    - add error unit tests for parse
    - add ingest contents tests
- ? Consider using a mixin for all of the viewsets
- ! add RESTful querying (contract/\<uuid>/account/, etc)
