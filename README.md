# GeneCo's Collections Software Experiment

"fun blurb here"

## Setup

`git clone [insert link here] && cd [name of repo]`

`docker compose build`

`docker compose up -d`

`docker compose exec -it col_api python manage.py migrate`

`docker compose exec -it col_api python manage.py createsuperuser`

Open [the server page](http://localhost:8999/admin/) to view the admin dash!

## To-dos!

- debate on auto-migrations
    - on one hand, ease of programming
    - on other hand, could break db if not ready?
    - on original hand, that's the whole point of migrations and test scripts??
